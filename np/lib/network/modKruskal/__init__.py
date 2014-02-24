'Network model using a modified kruskal algorithm'
# Import system modules
import itertools
import os
from time import localtime, strftime
import numpy
# Import custom modules
from np.lib import network, store, geometry_store, variable_store
# from np.model import Job


class MinimumNodeCountPerSubnetwork(variable_store.Variable):

    section = 'algorithm'
    option = 'minimum node count per subnetwork'
    c = dict(parse=int)
    default = 2
    units = 'nodes'


class ExistingNetworks(variable_store.Variable):

    section = 'network'
    option = 'existing networks'
    c = dict(parse=str, input=variable_store.inputFile)
    default = ''

class CandidateManager(object):
    """
    Class to manage the candidate node pairs in an efficient manner.
    The candidate node pairs (or segments) are the most memory consumptive
    component of modKruskal. 
    """
    dtype = [('i', 'uint16'), ('j', 'uint16'), ('w', 'f4')]

    def __init__(self, nodes, distanceFunction):
        'initialize the set of nodes and the index pair, distance array'
        self.nodes = nodes
        self.distanceFromNodeTuple = lambda index_tuple:\
                    distanceFunction(nodes[index_tuple[0]], nodes[index_tuple[1]])
        nodeIndexPairs = numpy.array(list(itertools.combinations(range(len(self.nodes)), 2)))
        self.nodeTuples = numpy.zeros((len(nodeIndexPairs)), dtype=CandidateManager.dtype)
        self.nodeTuples['i'] = nodeIndexPairs[:, 0]
        self.nodeTuples['j'] = nodeIndexPairs[:, 1]
        self.nodeTuples['w'] = numpy.apply_along_axis(self.distanceFromNodeTuple, 
                1, nodeIndexPairs)
        
        'for keeping track of target segments of projected nodes'
        self.targetSegmentLookup = {}
        

    def extendNodeTuples(self, tuples):
        """
        Used when existing nodes need to be related to new nodes
        (i.e. when existing nodes are projected onto network)
        """
        newNodeTuples = numpy.zeros((len(tuples)), dtype=CandidateManager.dtype)
        newNodeIndex = len(self.nodes)
        tupleIndex = 0
        for existingNodeIndex, newNode, targetSegment in tuples:
            self.nodes.append(newNode)
            newNodeTuples[tupleIndex]['i'] = existingNodeIndex
            newNodeTuples[tupleIndex]['j'] = newNodeIndex
            nodePairTuple = (existingNodeIndex, newNodeIndex)
            newNodeTuples[tupleIndex]['w'] = self.distanceFromNodeTuple(nodePairTuple)
            self.targetSegmentLookup[nodePairTuple] = targetSegment
            newNodeIndex += 1
            tupleIndex += 1
 
        self.nodeTuples = numpy.concatenate((newNodeTuples, self.nodeTuples))
        # nodeIndexPairs = numpy.array(list(itertools.combinations(range(len(networkNodes)), 2)))
        # segmentsByNodeIndex = numpy.zeros((len(nodeIndexPairs)), dtype=[('x', 'i2'), ('y', 'i2'), ('w', 'f4')])
        # segmentsByNodeIndex['i'] = nodeIndexPairs[:, 0]
        # segmentsByNodeIndex['j'] = nodeIndexPairs[:, 1]
        # distFromNodeIndexes = lambda index_tuple: computeDistance(networkNodes[index_tuple[0]], networkNodes[index_tuple[1]])
        # segmentsByNodeIndex['w'] = numpy.apply_along_axis(distFromNodeIndexes, 1, nodeIndexPairs)
        # segmentsByNodeIndex.sort(order='w')



class VariableStore(variable_store.VariableStore):

    variableClasses = [
        MinimumNodeCountPerSubnetwork,
        ExistingNetworks,
    ]

    def buildNetworkFromNodes(self, nodes, proj4, jobLogger=None):
        'Build a network using the given nodes'
        # If the spatial reference has units in meters,
        if '+units=m' in proj4:
            # Use euclidean distance
            computeDistance = network.computeEuclideanDistance
        else:
            # Use spherical distance
            computeDistance = network.computeSphericalDistance
        # Run algorithm given nodes
        net = self.buildNetworkFromSegments(*self.generateSegments(nodes, computeDistance, proj4), jobLogger=jobLogger)
        # Eliminate subnetworks that have too few real nodes
        minimumNodeCountPerSubnetwork = self.get(MinimumNodeCountPerSubnetwork)
        subnetFilter = lambda subnet: subnet.countNodes() >= minimumNodeCountPerSubnetwork
        net.filterSubnets(subnetFilter)
        return net

    def generateSegments(self, nodes, computeDistance, proj4):
        'Generate segment candidates connecting nodes to the existing grid'
        # Prepare
        segmentFactory = network.SegmentFactory(nodes, computeDistance, proj4)

        # Use more efficient CandidateManager for candidate segments
        candidateManager = CandidateManager(segmentFactory.getNodes(), computeDistance)

        net = network.Network(segmentFactory, useIndex=True)
        networkRelativePath = self.get(ExistingNetworks)
        # If we have existing networks,
        if networkRelativePath:
            # Reconstruct path
            networkArchivePath = os.path.join(self.state[0].getBasePath(), networkRelativePath)
            if not os.path.exists(networkArchivePath):
                raise variable_store.VariableError('Expected ZIP archive containing shapefile for existing networks')
            isValid, networkPath = store.unzip(networkArchivePath, 'shp')
            if not isValid:
                raise variable_store.VariableError('Could not find shapefile in ZIP archive for existing networks')
            # Load network
            networkProj4, networkGeometries = geometry_store.load(networkPath)[:2]
            networkCoordinatePairs = network.yieldSimplifiedCoordinatePairs(networkGeometries)
            # Prepare
            transform_point = geometry_store.get_transform_point(networkProj4, proj4)
            # Load existing network as a single subnet and allow overlapping segments
            net.addSubnet(network.Subnet([segmentFactory.getSegment(transform_point(c1[0], c1[1]), transform_point(c2[0], c2[1]), is_existing=True) for c1, c2 in networkCoordinatePairs]))
            # Add candidate segments that connect each node to its 
            # projection on the existing network
            projectedTuples = net.projectEfficient(candidateManager.nodes)
            candidateManager.extendNodeTuples(projectedTuples)

        return candidateManager, net 


    def buildNetworkFromSegments(self, candidateManager, net, jobLogger=None):
        """
        MAKE SURE THAT SEGMENTS WITH IDENTICAL COORDINATES CORRESPOND TO THE SAME OBJECT
        MAKE SURE THAT NODES WITH IDENTICAL COORDINATES CORRESPOND TO THE SAME OBJECT
        OTHERWISE WEIGHTS WILL NOT UPDATE
        """
        
        time_format = "%Y-%m-%d %H:%M:%S"
        if jobLogger:
            jobLogger.log("Building network from segments")

        print "%s Building network from segments" % strftime(time_format, localtime())

        # reporting variables
        numSegments = len(candidateManager.nodeTuples)
        completedSegments = 0
        nextReportThreshold = 0.10
        increment = 0.10

        # Cycle segments starting with the smallest first
        candidateManager.nodeTuples.sort(order='w')
        # keep a ref to the node array for convenience
        nodes = candidateManager.nodes
        for candidateTuple in candidateManager.nodeTuples:
            completionPercentage = completedSegments / float(numSegments)
            if completionPercentage > nextReportThreshold:
                time_format = "%Y-%m-%d %H:%M:%S"
                if jobLogger:
                    jobLogger.log("Processed %s (of %s) segments" % (completedSegments, numSegments))

                print "%s Processed %s (of %s) segments" % (strftime(time_format, localtime()), completedSegments, numSegments)
                nextReportThreshold += increment

            # Prepare
            node1Index, node2Index = candidateTuple['i'], candidateTuple['j']
            node1, node2 = nodes[node1Index], nodes[node2Index]
            # Prepare
            n1Weight, n2Weight, sWeight = node1.getWeight(), node2.getWeight(), candidateTuple['w']
            node1Qualifies = n1Weight >= sWeight or node1.getID() < 0 # canAfford or isFake
            node2Qualifies = n2Weight >= sWeight or node2.getID() < 0 # canAfford or isFake
            # If the segment qualifies,
            if node1Qualifies and node2Qualifies:
            
                # create a real segment at this point
                # TODO:  Worth creating a segment view???
                #        Might make this cleaner and save more space
                #        in the event that many node pairs "qualify"
                targetSegment = None
                indexTuple = (node1Index, node2Index)
                if candidateManager.targetSegmentLookup.has_key(indexTuple):
                    targetSegment = candidateManager.targetSegmentLookup[indexTuple]
                segment = net.segmentFactory.getSegment(node1.point.coords[0], 
                        node2.point.coords[0], segmentWeight=sWeight, targetSegment=targetSegment) 

                # Try to add the segment
                subnet = net.addSegment(segment)

                # If the segment was added,
                if subnet:
                    weight = n1Weight + n2Weight - sWeight
                    for node in subnet.cycleNodes():
                        node.setWeight(weight)

            completedSegments += 1


        time_format = "%Y-%m-%d %H:%M:%S"
        if jobLogger:
            jobLogger.log("processed %s (of %s) segments" % (completedSegments, numSegments))

        print "%s processed %s (of %s) segments" % (strftime(time_format, localtime()), completedSegments, numSegments)
        # Return
        return net


roots = [
    ExistingNetworks,
    MinimumNodeCountPerSubnetwork,
]
sections = [
    'network',
    'algorithm',
]
