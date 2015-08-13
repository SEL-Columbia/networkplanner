import sys
import os
import glob
import inspect
import ast
import astunparse
import json
import argparse
import networkx as nx
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
       len(ast_node.args) > 0 and\
       (type(ast_node.args[0]) == ast.Name or
        type(ast_node.args[0]) == ast.Attribute):
       return True
            
    return False
    

def get_get_var(ast_call):
    """
    get the variable name from the get_var node 
    """
    assert is_get_var(ast_call)
    name_or_attr = ast_call.args[0]
    if type(name_or_attr) == ast.Name:
       return name_or_attr.id
    elif type(name_or_attr) == ast.Attribute:
       return "{}.{}".format(name_or_attr.value.id, name_or_attr.attr)
    

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
    var_info = {'section':'', 'name':'', 'type':'OTHER', 'units':'',
                'default':'', 'dependencies':[]}

    cls_dict = cls.__dict__
    full_class_name = VS.getClassname(cls)
    if cls.dependencies is not None:
        var_info['dependencies'] =\
            sorted([VS.getClassname(dep_cls) for dep_cls in cls.dependencies])

    # class_name = full_class_name[full_class_name.rfind(".")+1:]
    var_info['name'] = full_class_name
    if 'section' in cls_dict:
        var_info['section'] = cls.section
    if 'units' in cls_dict:
        var_info['units'] = cls.units
    if 'default' in cls_dict:
        var_info['default'] = cls.default
    if 'aggregate' in cls_dict:
        fun_str = inspect.getsource(cls.aggregate)
        var_info['fun_src'] = fun_str
        var_info['type'] = "AGGREGATE"
    elif 'compute' in cls_dict:
        fun_str = inspect.getsource(cls.compute)
        var_info['fun_src'] = fun_str
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


def get_dependencies_from_fun(ast_fun):
    """
    return list of self.get(Variable) variables referenced
    within the function
    """
    for ast_node in ast.walk(ast_fun):
        if is_get_var(ast_node):
            yield get_get_var(ast_node)


def analyze_ast_variable(ast_cls, module_name):
    """
    Return dict of information gathered about the variable
    """
    var_info = {'name':'', 'type':'OTHER', 'units':'', 'default':'',
                'dependencies':[]}

    def get_full_var_name(var_name, module_name):
        if module_name and module_name != "__init__" and\
           not re.match(r"([^.]+)\.\w+", var_name):
            return "{}.{}".format(module_name, var_name)
        else:
            return var_name
            
    var_info['name'] = get_full_var_name(ast_cls.name, module_name)
    dependencies = set()
    
    cls_dict = member_dict(ast_cls)
    if 'units' in cls_dict:
        var_info['units'] = cls_dict['units']
    if 'default' in cls_dict:
        var_info['default'] = cls_dict['default']

    if 'aggregate' in cls_dict:
        fun_def = cls_dict['aggregate']
        var_info['fun_src'] = astunparse.unparse(fun_def)
        var_info['type'] = "AGGREGATE"
        dependencies = dependencies.union(
                           set([get_full_var_name(v, module_name) 
                                for v in get_dependencies_from_fun(fun_def)]))

    if 'compute' in cls_dict:
        fun_def = cls_dict['compute']
        var_info['fun_src'] = astunparse.unparse(fun_def)
        dependencies = dependencies.union(
                           set([get_full_var_name(v, module_name) 
                                for v in get_dependencies_from_fun(fun_def)]))

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

    # Find other curve type variables
    if re.match(r"\w+CurveType$", ast_cls.name):
        var_info['type'] = "CURVE_TYPE"
    elif re.match(r"\w+CurvePoints$", ast_cls.name):
        var_info['type'] = "CURVE_POINTS"
    elif re.match(r"\w+Curve$", ast_cls.name):
        var_info['type'] = "CURVE_FUN"

    # if the var doesn't have a compute/agg function then it's a leaf
    if not 'aggregate' in cls_dict or not 'compute' in cls_dict:
        var_info['type'] = "LEAF_VAR"
    
    var_info['dependencies'] = sorted(list(dependencies))

    return var_info

def output_csv(variable_dicts):
    """
    output the array of variables as a csv
    """
    print("{},{},{},{},{},{}".format("section", "name", "type", "default", "units", "dependencies") )
    for var in variable_dicts:
        print("{section},{name},{type},{default},{units},{dep_string}".format(**var))


parser = argparse.ArgumentParser(description="Analyze and report on metric model variables")
parser.add_argument("--from-model",
                    default=False,
                    action="store_true",
                    help="analyze by model name (rather than by dir)") 
parser.add_argument("--to-graph",
                    default=False,
                    action="store_true",
                    help="output as json network") 
parser.add_argument("model_dir_or_name",
                    help="model directory or name of model to be analyzed")

args = parser.parse_args()

# build up variable dicts
vars = []
if args.from_model:
    
    # import the model so that the subclasses of Variable are found
    mvModel = metric.getModel(args.model_dir_or_name)

    for var in all_subclasses(V):
        var_info = analyze_variable(var)
        var_info['dep_string'] = ";".join(var_info['dependencies'])
        vars.append(var_info)

elif os.path.isdir(args.model_dir_or_name):

    # for each file in path analyze all its variable classes 
    for py_file in glob.glob(args.model_dir_or_name + "/*.py"):
        module_name = os.path.basename(py_file)[:-3]
        with open(py_file) as pyf:
            ast_module = ast.parse(pyf.read())
        
        for ast_node in ast_module.body:
            if is_variable_class(ast_node):
                var_info = analyze_ast_variable(ast_node, module_name)
                if module_name == "__init__":
                    var_info['section'] = ""
                else:
                    var_info['section'] = module_name

                var_info['dep_string'] = ";".join(var_info['dependencies'])
                vars.append(var_info)
           
else:
    sys.stderr.write("Failed to read in valid model")
    sys.exit(1)

# write variable dicts appropriately
if args.to_graph:
    # todo import as networkx graph and write json
    g = nx.Graph()
    for var in vars:
        g.add_node(var['name'], **var)

    for var in vars:
        for dep in var['dependencies']:
            g.add_edge(var['name'], dep)

    pos=nx.fruchterman_reingold_layout(g)   
    for node in g.nodes():
        g.node[node]['x'] = pos[node][0]
        g.node[node]['y'] = pos[node][1]

    from networkx.readwrite import json_graph
    json_rep = json_graph.node_link_data(g) 
    print(json.dumps(json_rep, indent=4, sort_keys=True))
else:
    output_csv(vars) 
