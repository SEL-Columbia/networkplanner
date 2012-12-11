'Framework for building networks using different mathematical models'
# Import system modules
import itertools
import math
import shapely.ops
import shapely.geometry
import shapely.topology
from rtree import index
from time import localtime, strftime
# Import custom modules
from np.lib import store, geometry_store


# Define model wrappers

def getModelNames():
    return ['modKruskal']

def getModel(modelName):
    return store.getModel(__file__, modelName, getModelNames())

def getValueByOptionBySection(modelName):
    return getModel(modelName).VariableStore().getValueByOptionBySection()


# Define network classes

class Node(object):
    'A node'

    __slots__ = ('ID', 'x', 'y', 'longitude', 'latitude', 'weight', 'point', '__weakref__')
    
    def __init__(self, nodeID, (x, y), (longitude, latitude), weight):
        self.ID = nodeID
        self.x = x
        self.y = y
        self.longitude = longitude
        self.latitude = latitude
        self.weight = weight
        self.point = shapely.geometry.Point(x, y)

    # Need to override the get/set state methods so that nodes
    # can be pickled.  
    # By default pickling is done via the objects dict, but here
    # we're using slots to save space
    def __getstate__(self):
        return (self.ID, (self.x, self.y), (self.longitude, self.latitude), self.weight)

    def __setstate__(self, state):
        (self.ID, (self.x, self.y), (self.longitude, self.latitude), self.weight) = state
        self.point = shapely.geometry.Point(self.x, self.y)

    def __hash__(self):
        return hash(self.getCoordinates())

    def __repr__(self):
        if self.getID() >= 0:
            return 'node%s' % self.getID()
        else:
            return 'fake%s' % -self.getID()

    def __lt__(self, other):
        return self.getWeight() < other.getWeight()

    def __le__(self, other):
        return self.getWeight() <= other.getWeight()

    def __eq__(self, other):
        return self.getCoordinates() == other.getCoordinates()

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __gt__(self, other):
        return self.getWeight() > other.getWeight()

    def __ge__(self, other):
        return self.getWeight() >= other.getWeight()

    def getID(self):
        return self.ID

    def setID(self, nodeID):
        self.ID = nodeID

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWeight(self):
        return self.weight
    
    def setWeight(self, weight):
        self.weight = weight

    def getCoordinates(self):
        return self.getX(), self.getY()

    def getCommonCoordinates(self):
        return self.longitude, self.latitude


class Segment(object):
    'An undirected segment'

    __slots__ = ('node1', 'node2', 'weight', 'lineString', 'targetSegment', 'is_existing', '__weakref__')

    def __init__(self, node1, node2, weight, targetSegment=None, is_existing=False):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.lineString = shapely.geometry.LineString([node1.point.coords[0], node2.point.coords[0]])
        self.targetSegment = targetSegment
        self.is_existing = is_existing

    # Need to override the get/set state methods so that segments
    # can be pickled (for use in rtree).  
    # By default pickling is done via the objects dict, but here
    # we're using slots to save space
    def __getstate__(self):
        targetSegmentState = None
        if self.targetSegment:
            targetSegmentState = self.targetSegment.__getstate__()

        return (self.node1.__getstate__(), self.node2.__getstate__(),
                targetSegmentState, self.weight, self.is_existing)

    def __setstate__(self, state):
        self.node1 = Node.__new__(Node)
        self.node1.__setstate__(state[0])
        self.node2 = Node.__new__(Node)
        self.node2.__setstate__(state[1])
        self.targetSegment = None
        if not state[2] == None:
            self.targetSegment = Segment.__new__(Segment)
            self.targetSegment.__setstate__(state[2])

        self.weight = state[3]
        self.is_existing = state[4]
        self.lineString = shapely.geometry.LineString([self.node1.point.coords[0], self.node2.point.coords[0]])

    def __hash__(self):
        return hash(self.getCoordinates())
    
    def __repr__(self):
        node1 = self.getNode1()
        node2 = self.getNode2()
        return '%s-%s' % (node1, node2)

    def __lt__(self, other):
        return self.getWeight() < other.getWeight()

    def __le__(self, other):
        return self.getWeight() <= other.getWeight()

    def __eq__(self, other):
        return self.getCoordinates() == other.getCoordinates()

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __gt__(self, other):
        return self.getWeight() > other.getWeight()

    def __ge__(self, other):
        return self.getWeight() >= other.getWeight()

    def getNode1(self):
        return self.node1

    def getNode2(self):
        return self.node2

    def getNodes(self):
        return self.node1, self.node2

    def getSortedNodeIDs(self):
        return sorted([self.node1.getID(), self.node2.getID()])

    def getWeight(self):
        return self.weight

    def getCoordinates(self):
        'Return sorted coordinates to ensure that segments are undirected'
        return tuple(sorted((self.getNode1().getCoordinates(), self.getNode2().getCoordinates())))

    def getVector(self):
        lessCoordinates, moreCoordinates = self.getCoordinates()
        return lessCoordinates[0] - moreCoordinates[0], lessCoordinates[1] - moreCoordinates[1]

    def getTargetSegment(self):
        return self.targetSegment


class Network(object):
    'An undirected network'

    def __init__(self, segmentFactory, useIndex=False):
        # We will need the segmentFactory to generate segments on demand
        self.segmentFactory = segmentFactory
        # Prepare network
        self._subnets = []
        self._useIndex = useIndex

        if(self._useIndex):
            # These structures need to be updated for each 
            # segment we add to network.

            # Keep index of segments so we don't need to marshal them 
            # in/out of rtree.
            self._segments = {}
            self._idsBySegment = {}

            # Lookup table for subnets by segment coordinates. 
            # (need to update subnet lookups as they merge)
            self._subnetLookupBySegment = {}
            # rtree spatial index for intersection test speedup
            # setup properties first
            p = index.Property()
            p.index_capacity = 10
            p.leaf_capacity = 10
            p.near_minimum_overlap_factor = 3
            self._spatialIndex = index.Index(properties=p)

    def _getSegmentIntersections(self, segment):
        """
        Get the intersections within the network for the segment 
        Intersection may be a point or a collection of geoms (see Shapely for more)
        """
        resultsIter = self._spatialIndex.intersection(
                tuple(itertools.chain(*zip(*segment.lineString.xy))), 
                objects=False, 
                segment=True)
        initialIntersectingSegments = [self._segments[seg_id] 
                for seg_id in resultsIter]
        intersects  = (lambda newSegment: 
                segment.lineString.intersects(newSegment.lineString))
        intersectingSegments = filter(intersects, initialIntersectingSegments)
        intersection = lambda newSegment: (newSegment, 
                segment.lineString.intersection(newSegment.lineString))
        segmentIntersections = map(intersection, intersectingSegments)
        return segmentIntersections 

    def _getIntersectingSubnets(self, segment):
        """
        Get the subnets that intersect with the segment 
        and the number of intersections as a pair
        """
        segmentIntersections = self._getSegmentIntersections(segment) 

        # create unique subnet, intersection tuples
        subnetIntersections = {}
        for seg, intersection in segmentIntersections:
            subnet = self._subnetLookupBySegment[seg.getCoordinates()]
            if subnetIntersections.has_key(id(subnet)):
                # union the previous intersection geom with
                # this one (will reduce duplicate points)
                subnetIntersections[id(subnet)] = (subnet,
                        subnetIntersections[id(subnet)][1].union(intersection))
            else:
                subnetIntersections[id(subnet)] = (subnet, intersection)

        # create unique subnet, count tuples
        subnetCounts = {}
        for subnet, intersection in subnetIntersections.values():
            if isinstance(intersection, shapely.geometry.Point):
                # we have exactly one intersection
                subnetCounts[id(subnet)] = (subnet, 1)
            else:
                # we have more than one intersection
                assert len(intersection) > 1
                subnetCounts[id(subnet)] = (subnet, 2)

        # add the targetSegments subnet to the list of subnets if it does NOT
        # intersect it 
        # NOTE:  targetSegment is a workaround, so this may be removed if the
        # underlying problem is resolved.  See notes at bottom of file.
        targetSegment = segment.getTargetSegment()
        if targetSegment and not targetSegment.lineString.intersects(segment.lineString):
            # if the targetSegment does NOT intersect the segment
            # then it should NOT have been added to the list of intersecting segments
            # Remove this assertion if performance becomes an issue
            intersectingSegments = [segInts[0] for segInts in segmentIntersections]
            assert targetSegment not in intersectingSegments
            targetSubnet = self._subnetLookupBySegment[targetSegment.getCoordinates()]
            if subnetCounts.has_key(id(targetSubnet)):
                subnetCounts[id(targetSubnet)] = (targetSubnet,\
                        subnetCounts[id(targetSubnet)][1] + 1)
            else:
                subnetCounts[id(targetSubnet)] = (targetSubnet, 1)

        return subnetCounts.values()

    def filterSubnets(self, filterFunction):
        'Eliminate subnets that do NOT pass the filter'
        filteredSubnets = filter(filterFunction, self._subnets)
        if self._useIndex:
            for subnet in self.cycleSubnets():
                if subnet not in filteredSubnets:
                    self._deleteSubnetSegments(subnet)

        self._subnets = filteredSubnets

    def _deleteSubnetSegments(self, subnet):
        'Delete a subnets segments from the network'
        # Only Use Internally!!!
        assert self._useIndex
        for segment in subnet.cycleSegments():
            if (self._subnetLookupBySegment.has_key(segment.getCoordinates())):
                del(self._subnetLookupBySegment[segment.getCoordinates()])
                segmentId = self._idsBySegment[segment.getCoordinates()]
                del(self._segments[segmentId])
                del(self._idsBySegment[segment.getCoordinates()])
                self._spatialIndex.delete(segmentId, segment.lineString.bounds)


    def _updateIndex(self, subnet):
        'Update the Rtree and subnet lookup table with changes'
        # works for add/update (but not if segments are deleted)
        for segment in subnet.cycleSegments():
            # If the segment is not in the subnetLookup table, then it has 
            # NOT yet been added to the spatial index, in that case, Add it.  
            if (not self._subnetLookupBySegment.has_key(segment.getCoordinates())):
                segmentId = len(self._segments)
                self._spatialIndex.insert(segmentId, segment.lineString.bounds)
                self._idsBySegment[segment.getCoordinates()] = segmentId
                self._segments[segmentId] = segment

            self._subnetLookupBySegment[segment.getCoordinates()] = subnet

    def _addSegmentIndexed(self, newSegment):
        """
        Add a new segment to the network using index to get intersections; 
        return subnet if successful
        """

        #import pdb;
        #if(newSegment.node1.ID == 50 or newSegment.node1.ID == 110):
        #    pdb.set_trace()

        subnetCounts = self._getIntersectingSubnets(newSegment)

        mergingSubnets = []
        for subnet, intersectionCount in subnetCounts:
            if intersectionCount == 1:
                mergingSubnets.append(subnet)
            else:
                # the new segment would introduce a cycle
                # so simply return nothing
                return

        for subnet in mergingSubnets:
            self._subnets.remove(subnet)

        # Add the new subnet
        # subnet = Subnet(sum([x.segments for x in mergingSubnets], []) + [newSegment])
        subnet = self._constructSubnet(newSegment, mergingSubnets)
        self.addSubnet(subnet)
        # Return subnet
        return subnet

    # Placeholder for profiling
    def _constructSubnet(self, newSegment, mergingSubnets):
        return Subnet(sum([x.segments for x in mergingSubnets], []) + [newSegment])

    def _addSegment(self, newSegment):
        'Add a new segment to the network; return subnet if successful'
        # Initialize
        mergingSubnets = []
        # For each subnet,
        for subnet in self.cycleSubnets():
            # Compute intersection
            intersectionCategory = subnet.categorizeIntersection(newSegment)
            # If we have no intersection,
            if intersectionCategory == 0: 
                # Ignore subnet
                continue
            # If we have exactly one intersection,
            elif intersectionCategory == 1:
                # Add the subnet to the list of subnets to merge
                mergingSubnets.append(subnet)
            # If we have more than one intersection,
            else:
                # Ignore segment
                return
        # Remove subnets that we will merge
        for subnet in mergingSubnets:
            self._subnets.remove(subnet)
        # Add the new subnet
        subnet = Subnet(sum([x.segments for x in mergingSubnets], []) + [newSegment])
        self.addSubnet(subnet)
        # Return subnet
        return subnet

    def addSubnet(self, subnet):
        'Add subnet to list (update rtree if needed)'
        self._subnets.append(subnet)
        if(self._useIndex):
            self._updateIndex(subnet)

    def addSegmentViaCoordinates(self, node1Coordinates, node2Coordinates):
        self.addSegment(self.segmentFactory.getSegment(node1Coordinates, node2Coordinates))

    def addSegment(self, newSegment):
        'Add segment either using index method or not'
        if self._useIndex:
            return self._addSegmentIndexed(newSegment)
        else:
            return self._addSegment(newSegment)


    def cycleSegments(self):
        for subnet in self.cycleSubnets():
            for segment in subnet.cycleSegments():
                yield segment

    def cycleSubnets(self):
        for subnet in self._subnets:
            yield subnet

    def countSubnets(self):
        return len(self._subnets)

    def countSegments(self):
        return sum(x.countSegments() for x in self.cycleSubnets())

    # def saveSHP(self, targetPath):
        # geometry_store.save(store.replaceFileExtension(targetPath, 'shp'), self.proj4, [x.multiLineString for x in self.cycleSubnets()])

    def findClosestDistinctSegment(self, targetGeometry, multiLineString=None):
        'Find the segment that is closest but not equal to the given geometry'
        # If the user did not provide a multiLineString,
        if not multiLineString:
            # Construct multiLineString using all other segments
            multiLineString = shapely.geometry.MultiLineString([x.lineString.coords for x in self.cycleSegments() if not x.lineString.equals(targetGeometry)])
        # Compute distance to multiLineString
        distance = multiLineString.distance(targetGeometry)
        # If the distance is acceptable,
        if distance > 0:
            # Find the closest segment
            for sourceSegment in self.cycleSegments():
                if distance == targetGeometry.distance(sourceSegment.lineString):
                    return sourceSegment

    def projectEfficient(self, nodes):
        """
        Return list of tuples of form:
        (nodeIndex, connectingNode, targetSegment)
        representing the segments that connect the nodes 
        to the network. 
        This is intended to allow for a more efficient
        candidate segment representation.  
        """
        # Initialize
        time_format = "%Y-%m-%d %H:%M:%S"
        print "%s Generating projected segment candidates" % strftime(time_format, localtime())
        projectedTuples = []
        # Convert existing network into a multiLineString
        multiLineString = shapely.geometry.MultiLineString([x.lineString.coords for x in self.cycleSegments()])
        # For each node,
        for nodeIndex in range(len(nodes)):
            # Load point
            node = nodes[nodeIndex]
            point = node.point
            # Find the closest distinct segment in the network
            targetSegment = self.findClosestDistinctSegment(point, multiLineString)
            # If there is a segment that is close enough,
            if targetSegment:
                # Prepare
                lineString = targetSegment.lineString
                # Compute the projection of the point onto the targetSegment
                projectedPoint = lineString.interpolate(lineString.project(point))
                # Append the index/projected node/target tuple
                projectedTuples.append((nodeIndex, 
                    self.segmentFactory.getNode(projectedPoint.coords[0]), 
                        targetSegment))

        # Return
        return projectedTuples

    def project(self, nodes):
        'Return segments that connect the nodes to the network'
        # Initialize
        time_format = "%Y-%m-%d %H:%M:%S"
        print "%s Generating projected segment candidates" % strftime(time_format, localtime())
        projectedSegments = []
        # Convert existing network into a multiLineString
        multiLineString = shapely.geometry.MultiLineString([x.lineString.coords for x in self.cycleSegments()])
        # For each node,
        for node in nodes:
            # Load point
            point = node.point
            # Find the closest distinct segment in the network
            targetSegment = self.findClosestDistinctSegment(point, multiLineString)
            # If there is a segment that is close enough,
            if targetSegment:
                # Prepare
                lineString = targetSegment.lineString
                # Compute the projection of the point onto the targetSegment
                projectedPoint = lineString.interpolate(lineString.project(point))
                # Append the projectedSegment
                projectedSegments.append(self.segmentFactory.getSegment(point.coords[0], projectedPoint.coords[0], targetSegment=targetSegment))
        # Return
        return projectedSegments


class Subnet(object):
    'A set of related segments'

    def __init__(self, segments):
        self.segments = segments
        self.multiLineString = shapely.geometry.MultiLineString([x.lineString.coords for x in segments])

    def __repr__(self):
        return ', '.join(str(x) for x in self.cycleSegments())

    def categorizeIntersection(self, newSegment):
        'Figure out whether there are zero, single or multiple intersections'
        # Get intersectionCategory
        intersectionCategory = categorizeIntersection(self.multiLineString, newSegment.lineString)
        # Get targetSegment
        targetSegment = newSegment.getTargetSegment()
        # If the targetSegment is in our subnet and does not intersect our newSegment,
        if targetSegment and targetSegment in self.segments and not targetSegment.lineString.intersects(newSegment.lineString):
            # Add one to our intersection count
            intersectionCategory += 1
        # Return
        return intersectionCategory

    def cycleNodes(self):
        for segment in self.cycleSegments():
            for node in segment.getNodes():
                yield node

    def cycleSegments(self):
        for segment in self.segments:
            yield segment

    def countNodes(self):
        return len(set(self.cycleNodes()))

    def countSegments(self):
        return len(self.segments)


class SegmentFactory(object):
    'A factory for producing unique segments based on their coordinates'

    def __init__(self, nodes=None, computeWeight=None, proj4=geometry_store.proj4LL):
        # Initialze defaults
        if not nodes:
            nodes = []
        # Initialize index used to identify fake nodes
        self.nodeIndex = -1
        # Initialize dictionaries
        self.nodeByCoordinates = dict((node.getCoordinates(), Node(node.id, node.getCoordinates(), node.getCommonCoordinates(), node.metric)) for node in nodes)
        self.segmentByCoordinates = {}
        # Set
        self.computeWeight = computeWeight if computeWeight else lambda x, y: 1
        self.transform_point = geometry_store.get_transform_point(proj4)

    def getNodes(self):
        return self.nodeByCoordinates.values()

    def getSegment(self, node1Coordinates, node2Coordinates, segmentWeight=None, targetSegment=None, is_existing=False):
        # Sort coordinates
        segmentCoordinates = tuple(sorted((node1Coordinates, node2Coordinates)))
        # If we recognize the segment by its coordinates, return it
        if segmentCoordinates in self.segmentByCoordinates:
            return self.segmentByCoordinates[segmentCoordinates]
        # Load nodes
        node1, node2 = map(self.getNode, segmentCoordinates)
        # If there is no segmentWeight, use default
        if not segmentWeight:
            segmentWeight = self.computeWeight(node1, node2)
        # Create segment
        segment = Segment(node1, node2, segmentWeight, targetSegment, is_existing)
        # Store segment
        self.segmentByCoordinates[segmentCoordinates] = segment
        # Return
        return segment

    def getNode(self, coordinates):
        # If we recognize the node by its coordinates, return it
        if coordinates in self.nodeByCoordinates:
            return self.nodeByCoordinates[coordinates]
        # Expand coordinates
        x, y = coordinates
        # Create a fake node
        node = Node(self.nodeIndex, (x, y), self.transform_point(x, y), 0)
        self.nodeIndex -= 1
        # Store node
        self.nodeByCoordinates[coordinates] = node
        # Return
        return node


def categorizeIntersection(multiLineString, lineString):
    if lineString.disjoint(multiLineString):
        # We have no intersections
        return 0
    # Try to get the intersection
    try:
        intersection = lineString.intersection(multiLineString)
    except shapely.topology.TopologicalError:
        # Prepare generator
        partialIntersectionGenerator = (lineString.intersection(x) for x in multiLineString.geoms if lineString.intersects(x))
        # Get first intersection
        intersection = partialIntersectionGenerator.next()
        # For each partialIntersection,
        for partialIntersection in partialIntersectionGenerator:
            # Merge partialIntersection
            intersection = intersection.union(partialIntersection)
            # If we have more than one intersection,
            if not isinstance(intersection, shapely.geometry.Point):
                break
    # If we have exactly one intersection,
    if isinstance(intersection, shapely.geometry.Point):
        return 1
    # We have more than one intersection
    return 2


def simplifyGeometry(geometry):
    # If we have a LineString,
    if isinstance(geometry, shapely.geometry.LineString):
        return geometry.simplify(0)
    # If we have a MultiLineString,
    elif isinstance(geometry, shapely.geometry.MultiLineString):
        return shapely.ops.linemerge(geometry).simplify(0)
    # Otherwise,
    else:
        # Raise exception
        raise ValueError('Unexpected geometry type: %s' % geometry.type)


def mergeGeometries(geometries):
    return reduce(lambda x, y: x.union(y), geometries)


def yieldSimplifiedCoordinatePairs(geometries):
    # Simplify individually first, then merge and simplify the merged geometry
    x = simplifyGeometry(mergeGeometries(simplifyGeometry(x) for x in geometries))
    # Prepare
    if isinstance(x, shapely.geometry.LineString):
        geometries = [x]
    elif isinstance(x, shapely.geometry.MultiLineString):
        geometries = x.geoms
    else:
        raise ValueError('Unexpected geometry type: %s' % geometry.type)
    # For each geometry,
    for geometry in geometries:
        # For each coordinatePack,
        for coordinateIndex in xrange(len(geometry.coords) - 1):
            # Yield
            yield geometry.coords[coordinateIndex], geometry.coords[coordinateIndex + 1]


def computeEuclideanDistance(node1, node2):
    return node1.point.distance(node2.point)


def computeSphericalDistance(node1, node2):
    """
    http://en.wikipedia.org/wiki/Great-circle_distance
    """
    # Define
    convertDegreesToRadians = lambda x: x * math.pi / 180
    # Load
    longitude1, latitude1 = map(convertDegreesToRadians, node1.getCommonCoordinates())
    longitude2, latitude2 = map(convertDegreesToRadians, node2.getCommonCoordinates())
    # Initialize
    longitudeDelta = longitude2 - longitude1
    earthRadiusInMeters = 6371010
    # Prepare
    y = math.sqrt(math.pow(math.cos(latitude2) * math.sin(longitudeDelta), 2) + math.pow(math.cos(latitude1) * math.sin(latitude2) - math.sin(latitude1) * math.cos(latitude2) * math.cos(longitudeDelta), 2))
    x = math.sin(latitude1) * math.sin(latitude2) + math.cos(latitude1) * math.cos(latitude2) * math.cos(longitudeDelta)
    # Return
    return earthRadiusInMeters * math.atan2(y, x)


"""
Someone should fix the following workarounds after GEOS fixes their bugs.


Issue: The Point resulting from MultiLineString.interpolate() is sometimes very close to the correct Point but does not intersect MultiLineString.
Workaround: Since we need to count the number of intersections and since this discrepancy does not always happen, we cannot simply detect whether the distance of the Point to the MultiLineString approximately matches the distance of the Point to the projected Point.  Instead, we record which segment to which we were trying to project and record that segment as the targetSegment.  Then, we use the targetSegment to help us determine whether the projectedSegment is intersecting a given Subnet.
How to undo workaround: Remove all references to targetSegment


Issue: The Point resulting from MultiLineString.interpolate() is sometimes plain wrong.
Workaround: Check whether the resulting Point is within an acceptable distance from the MultiLineString.  If it is not, then cycle through each LineString of the MultiLineString to see if we can find one whose distance from the Point matches the distance of the MultiLineString from the Point.  Then project the Point onto that LineString.
How to undo workaround: Rewrite Network.project() to use MultiLineString.interpolate()


Issue: Intersecting a MultiLineString and a LineString sometimes throws a ValueError exception.
Workaround: If intersecting a MultiLineString and a LineString throws a ValueError, then construct a new MultiLineString using a list of LineStrings from the old MultiLineString that intersect the original LineString and determine the intersection between the new MultiLineString and the original LineString.
How to undo workaround: Remove the try-except block surrounding LineString.intersection(MultiLineString)
"""
