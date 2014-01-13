import sys, csv, collections, json, os
# set basepath to parent dir for np imports
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)
from np.lib import metric, dataset_store, geometry_store, variable_store as VS
import argparse


"""
Utility to run only the metric model on a set of demand
nodes given a set of model parameters.  
This allows more rapid feedback on demand and model changes
"""

def getNodes(proj4, nodePacks):
    """
    Return the dataset_store.Node objects corresponding to
    the nodePacks (transformed into our "universal" coordinate
    system: longlat WGS84)
    """
    nodes = []
    transform_point = geometry_store.get_transform_point(proj4)
    # Check for duplicates
    nodePacksByCoordinates = collections.defaultdict(list)
    for nodePack in nodePacks:
        coordinates = float(nodePack['x']), float(nodePack['y'])
        nodePacksByCoordinates[coordinates].append(nodePack)
    # For each row,
    for coordinates, nodePacks in nodePacksByCoordinates.iteritems():
        # If there are duplicates,
        if len(nodePacks) > 1:
            print 'Duplicate nodes' 
            for nodePack in nodePacks:
                print '(%s) %s' % (str(coordinates), nodePack)
        # Add
        longitude, latitude = transform_point(*coordinates)
        nodes.append(dataset_store.Node(coordinates, (longitude, latitude), nodePacks[0]))
    
    return nodes


# Run DemandBuilder
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run metric model on demand nodes")
    parser.add_argument('model_name', choices=metric.getModelNames(),
                        help="model definition to run")
    parser.add_argument('model_params', type=argparse.FileType('r'),
                        help="model parameters json file")
    parser.add_argument('input_nodes', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="csv file of nodes (lat,lon,population,...)")
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, 
                        help="csv output of model run")
    parser.add_argument("-t", "--header-type", 
                        choices=[VS.HEADER_TYPE_SECTION_OPTION, 
                                 VS.HEADER_TYPE_ALIAS,
                                 VS.HEADER_TYPE_SHORT_NAME], 
                        default=VS.HEADER_TYPE_ALIAS,
                        help="the output file header field name type")                       
                        
    args = parser.parse_args()

    # setup model
    metricModel = metric.getModel(args.model_name)

    metricValueByOptionBySection = json.load(args.model_params)

    """
    // Sample Model Parameter JSON
    metricValueByOptionBySection = {
        'demand (household)': 
            {'household unit demand per household per year': 50}
    }
    """

    jobVS = metricModel.VariableStore(metricValueByOptionBySection)
    
    # process input stream nodes
    proj4, nodePacks = dataset_store.digestNodesFromCSVStream(args.input_nodes)  
    nodes = getNodes(proj4, nodePacks)

    # run the model on each node
    # NOTE:  No nodes should be "fake" at this point, but this is 
    #        here just for consistency with the rest of NetworkPlanner
    node_gen = (node for node in nodes if not node.is_fake)
    for node in node_gen:
        # Load node-level configuration
        nodeVS = metricModel.VariableStore(node.getValueByOptionBySection(), jobVS)
        # Save results
        node.metric = nodeVS.get(metricModel.Metric)
        node.output = nodeVS.getValueByOptionBySection()

    # prep the csv output stream
    csvWriter = csv.writer(args.outfile)

    # use last node as basis for header
    nodeInput = node.input
    nodeOutput = node.output
    # get the section/option values in order from both input/output 
    headerPacks = [('', key) for key in sorted(nodeInput)] # handle the aliases?  
    for section, valueByOption in sorted(nodeOutput.iteritems(), 
                                         key=lambda x: 
                                         metricModel.sections.index(x[0])):
        for option in sorted(valueByOption):
            headerPacks.append((section, option))

    headerPacksToNames = VS.getFieldNamesForHeaderPacks(metricModel, 
                            headerPacks, args.header_type)

    csvWriter.writerow([headerPacksToNames[(section, option)] for 
                        section, option in headerPacks])
    """
    csvWriter.writerow([sectionOptionToAlias[(section, option)] if section 
                        else option.capitalize() 
                        for section, option in headerPacks])
    """

    node_gen = (node for node in nodes if not node.is_fake)
    for node in node_gen:
        # Write row for all node's values (by section, option)
        csvWriter.writerow([node.output.get(section, {}).get(option, '') if section else node.input.get(option, '') for section, option in headerPacks])


    # TODO:  do anything with jobVS?  Output summary stats?  

