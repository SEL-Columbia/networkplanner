import sys, os

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

    sys.stdout.write("class,alias,section,option,units,default,dependencies\n")
    for var in variableSet:
        clazz = VS.getClassname(var)
        alias = VS.getAlias(var)
        depClasses = []
        if var.dependencies != None:
            depClasses = [VS.getClassname(dep) for dep in var.dependencies]

        sys.stdout.write("%s,%s,%s,%s,%s,%s,%s\n" % (clazz, alias, var.section, 
                         var.option, var.units, var.default, ";".join(depClasses)))
        
