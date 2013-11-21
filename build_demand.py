import sys, csv, collections, json
from np.lib import metric, dataset_store, geometry_store


def getNodes(proj4, nodePacks):
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

    if (len(sys.argv) < 3):
        sys.stderr.write("example usage:  cat node.csv | python build_demand.py model_name model_params.json\n")
        sys.exit()

    # setup model
    model_name = sys.argv[1] 
    model_params_file = sys.argv[2] 
    metricModel = metric.getModel(model_name)

    metricValueByOptionBySection = json.load(open(model_params_file, 'r'))

    """
    metricValueByOptionBySection = {
        'demand (household)': 
            {'household unit demand per household per year': 50}
    }
    """

    jobVS = metricModel.VariableStore(metricValueByOptionBySection)
    
    # process input stream nodes
    proj4, nodePacks = dataset_store.digestNodesFromCSVStream(sys.stdin)  
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
    csvWriter = csv.writer(sys.stdout)
    # use last node as basis for header
    nodeInput = node.input
    nodeOutput = node.output
    headerPacks = [('', key) for key in sorted(nodeInput)] # handle the aliases?  
    for section, valueByOption in sorted(nodeOutput.iteritems(), key=lambda x: metricModel.sections.index(x[0])):
        for option in sorted(valueByOption):
            headerPacks.append((section, option))

    csvWriter.writerow(['%s > %s' % (section.capitalize(), option.capitalize()) if section else option.capitalize() for section, option in headerPacks])

    node_gen = (node for node in nodes if not node.is_fake)
    for node in node_gen:
        # Write row for all node's values (by section, option)
        csvWriter.writerow([node.output.get(section, {}).get(option, '') if section else node.input.get(option, '') for section, option in headerPacks])


    # TODO:  do anything with jobVS?  What's done with it when returned from applyMetric in scenario.run?
