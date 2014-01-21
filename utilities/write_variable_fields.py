import sys, os
import inspect

# Prevents this script from failing when output is piped
# to another process
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

from np.lib import metric
from np.lib import variable_store as VS
from np import util

if __name__ == '__main__':

    if (len(sys.argv) < 2):
        sys.stderr.write("example usage:  python write_variable_fields.py model [variable]\n")
        sys.exit()

    # setup model
    model = sys.argv[1]
    variable = None
    if len(sys.argv) > 2:
        variable = sys.argv[2] 

    mvModel = metric.getModel(model)
    variableSet = []
    if variable:
        modelVar = util.getSubModuleFromString(mvModel, variable)
        variableSet = VS.getRelatedVariables(modelVar)
    else:
        # no variable parameter, get all vars for the model
        variableSet, roots = VS.gatherVariables(mvModel.VariableStore)

    sys.stdout.write("file,class,alias1,alias2,section,option,units,default,dependencies\n")
    for var in variableSet:
        filename = inspect.getfile(var).replace('.pyc', '.py') 
        clazz = VS.getClassname(var)
        alias = VS.getAlias(var)
        alias1 = "" if not var.aliases or len(var.aliases) < 1 else var.aliases[0] 
        alias2 = "" if not var.aliases or len(var.aliases) < 2 else var.aliases[1] 

        depClasses = []
        if var.dependencies != None:
            depClasses = [VS.getClassname(dep) for dep in var.dependencies]

        sys.stdout.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (filename, clazz, alias1, alias2, var.section, 
                         var.option, var.units, var.default, ";".join(depClasses)))
        
