import sys, os
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

from np.lib import metric
from np.lib import variable_store as VS
import pydot

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
        node = pydot.Node(VS.getName(node_var, 'id'), style='filled', 
                          fillcolor=fill_color)
        node.set_label(VS.getName(node_var, nameType))
        graph.add_node(node)

    # Now add edges
    for var_to in variableGraph:
        for var_from in var_to[1]:
            node_from = graph.get_node(VS.getName(var_from, 'id'))[0]
            node_to = graph.get_node(VS.getName(var_to[0], 'id'))[0]
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
    dependencies = VS.buildOrderedDependencies(modelVar)
    graph = buildPyDotGraph(dependencies, nameType)
    
    graph.write(outfile, format="png")
    

    
