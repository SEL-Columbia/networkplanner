import sys, os
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

from np.lib import metric
from np.lib.metric import mvMax5
import pydot

BASE_PATH = "np.lib.metric"

def getSubModuleFromString(parent, subModuleString):
    """
    Get the submodule from the parent module
    parent:  a python module
    subModuleString:  a 'dot-notated' sub-module string (i.e. "module1.class1")
    """
    moduleList = subModuleString.split(".")
    subMod = getattr(parent, moduleList[0])
    if len(moduleList) == 1:
        return subMod
    else:
        return getSubModuleFromString(subMod, ".".join(moduleList[1:]))


def getAlias(varClass):
    """
    Get alias as first item in list of aliases if there
    else just use lower-case option
    """
    if varClass.aliases != None or len(varClasses) > 0:
        return varClass.aliases[0]
    else:
        return varClass.option.capitalize()

def getClassname(varClass):
    """
    Outputs classname minus BASE_PATH
    """
    moduleName = varClass.__module__.replace(BASE_PATH + ".", "")
    return "%s.%s" % (moduleName, varClass.__name__)
 
def getClassnameForId(varClass):
    """
    Outputs classname minus BASE_PATH with underscores over dots
    (since pydot does funky escaping of dots)
    """
    return getClassname(varClass).replace(".", "_") 

def getOption(varClass):
    return "%s\n%s" % (varClass.section, varClass.option)
    
def getName(varClass, nameType):

    nameFunctions = {
        'id': getClassnameForId,
        'alias': getAlias,
        'option': getOption,
        'class': getClassname
        }

    return nameFunctions[nameType](varClass)


def buildOrderedDependencies(varClass):
    """
    Output graph of dependencies in Breadth-First order
    Graph is represented as 
      [(Variable, [dependency,...]),...] 
    """

    classDependencies = []

    dependencyQueue = [varClass]
    visited = set()
    visited.add(varClass) #add root to visited set
    while len(dependencyQueue) > 0:
        vCls = dependencyQueue.pop()
        depList = [] #collect the dependencies
        # check if dependencies is None
        if vCls.dependencies != None:
            for cls in (dep for dep in vCls.dependencies if dep not in visited):
                # insert in front so list acts as queue
                dependencyQueue.insert(0, cls)
                visited.add(cls)
            depList = [dep for dep in vCls.dependencies if vCls.dependencies]

        classDependencies.append((vCls, depList))
    return classDependencies


def buildPyDotGraph(variableGraph, nameType):
    """
    build up Pydot graph of nodes (Variables) and edges (Variable Dependencies)
    """
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')

    # First add nodes
    for var in variableGraph:
        fill_color = "#AA9999"
        # fill based on whether var is a leaf (i.e. dependencies are empty)
        if len(var[1]) == 0:
            fill_color = "#9999AA"

        node_var = var[0]
        node = pydot.Node(getName(node_var, 'id'), style='filled', 
                          fillcolor=fill_color)
        node.set_label(getName(node_var, nameType))
        graph.add_node(node)

    # Now add edges
    for var_to in variableGraph:
        for var_from in var_to[1]:
            node_from = graph.get_node(getName(var_from, 'id'))[0]
            node_to = graph.get_node(getName(var_to[0], 'id'))[0]
            graph.add_edge(pydot.Edge(node_from, node_to))

    return graph


if __name__ == '__main__':

    if (len(sys.argv) < 4):
        sys.stderr.write("example usage:  python model_demand_dependencies.py model variable outfile [name_type]")
        sys.exit()

    # setup model
    model = sys.argv[1]
    variable = sys.argv[2] 
    outfile = sys.argv[3]
    nameType = "alias"
    if len(sys.argv) == 5:
        nameType = sys.argv[4]

    mvModel = metric.getModel(model)
    modelVar = getSubModuleFromString(mvModel, variable)
    dependencies = buildOrderedDependencies(modelVar)
    graph = buildPyDotGraph(dependencies, nameType)
    
    graph.write(outfile, format="png")
    

    
