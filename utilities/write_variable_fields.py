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

    sys.stdout.write("file,class,alias,section,option,short_section,short_option,units,default,dependencies\n")
    for var in variableSet:
        filename = inspect.getfile(var).replace('.pyc', '.py') 
        clazz = VS.getClassname(var)
        alias = VS.getAlias(var)

        short_section = ""
        short_option = ""
        if hasattr(var, 'short_section'):
            short_section = var.short_section 
        if hasattr(var, 'short_option'):
            short_option = var.short_option

        depClasses = []
        if var.dependencies != None:
            depClasses = [VS.getClassname(dep) for dep in var.dependencies]

        sys.stdout.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (filename, clazz, alias, var.section, 
                         var.option, short_section, short_option, var.units, var.default, ";".join(depClasses)))
        
