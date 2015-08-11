import sys
import os
import glob
import inspect
import ast
import argparse
import re
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

from np.lib import variable_store as VS
from np.lib.variable_store import Variable as V
from np.lib import metric 

def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                       for g in all_subclasses(s)]

def unindent_fun(fun_str):
    """
    Takes compute function as string and returns
    unindented version (suitable for ast parsing)
    """
    lines = fun_str.splitlines()
    def_line = lines[0]
    # find indentation to strip from rest of lines
    # assumes each line uses same char for indentation
    start_def = def_line.find("def")
    unind_fun = "\n".join([line[start_def:] for line in lines])
    return unind_fun


def is_get_var(ast_node):
    """
    is ast call a get variable function
    """
    # Note:  self is really an attribute (hence the ast.Attribute test below)
    if type(ast_node) == ast.Call and type(ast_node.func) == ast.Attribute and\
       type(ast_node.func.value) == ast.Name and\
       ast_node.func.value.id == 'self' and ast_node.func.attr == 'get' and\
       len(ast_node.args) > 0 and type(ast_node.args[0]) == ast.Name:
       return True
            
    return False
    

def is_simple_op(ast_node):
    """
    determines if the node represents a parse tree with only binary ops and 
    get vars or constants
    """
    if type(ast_node) == ast.BinOp:
        return is_simple_op(ast_node.left) and \
               is_simple_op(ast_node.right)

    if type(ast_node) == ast.Call:
        return is_get_var(ast_node)

    if type(ast_node) == ast.Num:
        return True

    return False


def is_variable_class(ast_node):
    """
    Determine if node is a 'Variable' class definition

    NOTE:  For now this only checks whether the class inherits 
    from V (which by convention is the alias we assign the Variable class)
    """
    if not type(ast_node) == ast.ClassDef:
        return False

    base_name_ids = [base.id for base in ast_node.bases]
    if 'V' in base_name_ids:
        return True

    return False
    

def analyze_variable(cls):
    """
    Return dict of information gathered about the variable
    """
    var_info = {'name':'', 'type':'OTHER', 'units':'', 'default':''}

    cls_dict = cls.__dict__
    full_class_name = VS.getClassname(cls)
    # class_name = full_class_name[full_class_name.rfind(".")+1:]
    var_info['name'] = full_class_name
    if 'units' in cls_dict:
        var_info['units'] = cls.units
    if 'default' in cls_dict:
        var_info['default'] = cls.default
    if 'aggregate' in cls_dict:
        var_info['type'] = "AGGREGATE"
    elif 'compute' in cls_dict:
        compute_fun_str = inspect.getsource(cls.compute)
        unindented = unindent_fun(compute_fun_str)
        fun_ast = ast.parse(unindented)
        fun_def = fun_ast.body[0]
        for i in range(len(fun_def.body)):
            node = fun_def.body[i]
            if type(node) == ast.Expr and type(node.value) == ast.Str:
                pass # it's a docstring
            elif type(node) == ast.Return:
                if is_simple_op(node.value):
                    var_info['type'] = "SINGLE_STMT_SIMPLE"
                else:
                    var_info['type'] = "SINGLE_STMT_OTHER"
            break
    else:
        var_info['type'] = "LEAF_VAR"

    return var_info

def member_dict(ast_cls):
    """
    Return dict of member assignments (including functions)
    """
    cls_dict = {}

    # may want to define things to do with other types here
    val_lookup = {ast.Num: lambda node: node.n, 
                  ast.Str: lambda node: node.s}

    def get_val_for_node(node):
        if type(node) in val_lookup:
           return val_lookup[type(node)](node)
        else:
            return node

    for node in ast_cls.body:
        if type(node) == ast.Assign:
            # map the target to its value (or node if it's not a simple type)
            value = get_val_for_node(node.value)
            # may be more than one target
            for target in node.targets:
                cls_dict[target.id] = value

        if type(node) == ast.FunctionDef:
            cls_dict[node.name] = node
                
    return cls_dict

def analyze_ast_variable(ast_cls):
    """
    Return dict of information gathered about the variable
    """
    var_info = {'name':'', 'type':'OTHER', 'units':'', 'default':''}

    var_info['name'] = ast_cls.name 
    cls_dict = member_dict(ast_cls)
    if 'units' in cls_dict:
        var_info['units'] = cls_dict['units']
    if 'default' in cls_dict:
        var_info['default'] = cls_dict['default']
    if re.match(r"\w+CurveType$", ast_cls.name):
        var_info['type'] = "CURVE_TYPE"
    elif re.match(r"\w+CurvePoints$", ast_cls.name):
        var_info['type'] = "CURVE_POINTS"
    elif re.match(r"\w+Curve$", ast_cls.name):
        var_info['type'] = "CURVE_FUN"
    elif 'aggregate' in cls_dict:
        var_info['type'] = "AGGREGATE"
    elif 'compute' in cls_dict:
        fun_def = cls_dict['compute']
        if ast.dump(fun_def).find("interpolate") > 0:
            var_info['type'] = "CURVE_INTERPOLATE"
        else:
            for i in range(len(fun_def.body)):
                node = fun_def.body[i]
                if type(node) == ast.Expr and type(node.value) == ast.Str:
                    pass # it's a docstring
                elif type(node) == ast.Return:
                    if is_simple_op(node.value):
                        var_info['type'] = "SINGLE_STMT_SIMPLE"
                    else:
                        var_info['type'] = "SINGLE_STMT_OTHER"
                break
    else:
        var_info['type'] = "LEAF_VAR"

    return var_info

parser = argparse.ArgumentParser(description="Analyze and report on metric model variables")
parser.add_argument("--from-model", 
                    default=False,
                    action="store_true", 
                    help="analyze by model name (rather than by dir)") 
parser.add_argument("model_dir_or_name",
                    help="model directory or name of model to be analyzed")

args = parser.parse_args()

if args.from_model:
    
    # import the model so that the subclasses of Variable are found
    mvModel = metric.getModel(args.model_dir_or_name)

    print("{},{},{},{}".format("name", "type", "default", "units") )
    for var in all_subclasses(V):
        var_info = analyze_variable(var)
        print("{name},{type},{default},{units}".format(**var_info))

elif os.path.isdir(args.model_dir_or_name):

    print("{},{},{},{}".format("name", "type", "default", "units") )
    # for each file in path analyze all its variable classes 
    for py_file in glob.glob(args.model_dir_or_name + "/*.py"):
        module_name = os.path.basename(py_file)[:-3]
        with open(py_file) as pyf:
            ast_module = ast.parse(pyf.read())
        
        for ast_node in ast_module.body:
            if is_variable_class(ast_node):
                var_info = analyze_ast_variable(ast_node)
                if module_name == "__init__":
                    print("{name},{type},{default},{units}".format(**var_info))
                else: 
                    print("{}.{name},{type},{default},{units}".\
                          format(module_name, **var_info))
            
else:
    sys.stderr.write("Failed to read in valid model")
    sys.exit(1)
