import sys, os
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

if __name__ == '__main__':

    if(len(sys.argv) < 2): 
        sys.stderr.write("example usage:  python write_all_variables.py model\n")
        sys.exit()

    # setup model
    model = sys.argv[1]
    # import the model so that the subclasses of Variable are found
    mvModel = metric.getModel(model)

    for var in all_subclasses(V):
        print VS.getClassname(var)
