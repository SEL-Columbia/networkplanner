import sys, os
import inspect
import ast
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

def analyze_variable(cls):
    """
    Return dict of information gathered about the variable
    """
    var_info = {'name':'', 'type':'OTHER', 'units':'', 'default':''}

    cls_dict = cls.__dict__
    var_info['name'] = VS.getClassname(cls)
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


if __name__ == '__main__':

    if(len(sys.argv) < 2): 
        sys.stderr.write("example usage:  python analyze_model_vars.py model\n")
        sys.exit()

    # setup model
    model = sys.argv[1]
    # import the model so that the subclasses of Variable are found
    mvModel = metric.getModel(model)

    print("{},{},{},{}".format("units", "default", "type", "name") )
    for var in all_subclasses(V):
        var_info = analyze_variable(var)
        print("{units},{default},{type},{name}".format(**var_info))
