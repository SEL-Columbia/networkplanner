# Import system modules
import unittest
# Import custom modules
from np.lib import network


class TestNetworkRtree(unittest.TestCase):

    def setUp(self):
        # Initialize
        self.segmentFactory = network.SegmentFactory(proj4='+proj=utm +zone=28 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
        self.net = network.Network(self.segmentFactory, useIndex=True)

    def testIntersectingSegmentsViaRTree(self):
        """
        Test touches and crosses cases
        Create network that looks like:
          
          |     /
          |    /
          |   /
          |  /
          | /
          |/
        
        And then check which of those segments intersect with
        various test segments
        """

        verticalSegments = [self.segmentFactory.getSegment((0, y), (0, y + 1)) for y in xrange(0, 5)]
        slopeOfOneSegments = [self.segmentFactory.getSegment((v, v), (v + 1, v + 1)) for v in xrange(0, 5)]
        for segment in verticalSegments:
            self.net.addSegment(segment)
        for segment in slopeOfOneSegments:
            self.net.addSegment(segment)

        segmentExtractor = lambda segmentIntersection: segmentIntersection[0]

        'Test that a segment intersecting the origin intersects 2 segments'
        results = self.net._getSegmentIntersections(self.segmentFactory.getSegment((-1, 0), (1, 0)))
        originSegments = map(segmentExtractor, results)
        assert originSegments == [verticalSegments[0], slopeOfOneSegments[0]]

        'Test that a segment intersects the top most segments'
        results = self.net._getSegmentIntersections(self.segmentFactory.getSegment((0, 5), (5, 5)))
        topMostSegments = map(segmentExtractor, results)
        assert topMostSegments == [verticalSegments[4], slopeOfOneSegments[4]]

        'Test that a segment intersect a segment by crossing it in the middle'
        results = self.net._getSegmentIntersections(self.segmentFactory.getSegment((4, 5), (5, 4)))
        topRightSegment = map(segmentExtractor, results)
        assert topRightSegment == [slopeOfOneSegments[4]]

        
    def testIntersectingSubnetsViaRTree(self):
        """
        Test appropriate subnets are intersected correct number of times
        Create network of subnets that looks like:
          
          |     /     |
          |    /      |
          |   /       |
          |  /        |
          | /         |
          |/          |
        
        """
      
        subnetA = [self.segmentFactory.getSegment((0, y), (0, y + 1)) for y in xrange(0, 5)]
        subnetA.extend([self.segmentFactory.getSegment((v, v), (v + 1, v + 1)) for v in xrange(0, 5)])
        verticalSegments = [self.segmentFactory.getSegment((10, y), (10, y + 1)) for y in xrange(0, 5)]

        # Add segments from all the above (should result in 2 subnets)
        self.net.addSubnet(network.Subnet(subnetA))
        for segment in verticalSegments:
            self.net.addSegment(segment)

        'Test that there are 2 subnets'
        assert self.net.countSubnets() == 2

        'Test that we intersect with a subnet once'
        subnetCounts = self.net._getIntersectingSubnets(self.segmentFactory.getSegment((9, 4.5), (11, 4.5)))
        assert len(subnetCounts) == 1
        assert subnetCounts[0][1] == 1

        'Test that we intersect with 2 subnets (each in only one place)'
        subnetCounts = self.net._getIntersectingSubnets(self.segmentFactory.getSegment((1, 4.5), (11, 4.5)))
        assert len(subnetCounts) == 2
        assert len(filter(lambda sc: sc[1] == 1, subnetCounts)) == 2

        'Test that we intersect with 1 subnet in 2 places'
        subnetCounts = self.net._getIntersectingSubnets(self.segmentFactory.getSegment((-1, 4.5), (5, 4.5)))
        assert len(subnetCounts) == 1
        assert subnetCounts[0][1] == 2

    def testSubnetFilter(self):
        """
        Test that subnetFilter works
        """
      
        subnetA = [self.segmentFactory.getSegment((0, y), (0, y + 1)) for y in xrange(0, 5)]
        subnetA.extend([self.segmentFactory.getSegment((v, v), (v + 1, v + 1)) for v in xrange(0, 5)])
        verticalSegments = [self.segmentFactory.getSegment((10, y), (10, y + 1)) for y in xrange(0, 5)]

        # Add segments from all the above (should result in 2 subnets)
        self.net.addSubnet(network.Subnet(subnetA))
        for segment in verticalSegments:
            self.net.addSegment(segment)

        'Test that there are 2 subnets'
        assert self.net.countSubnets() == 2

        subnetFilter = lambda subnet: subnet.countSegments() >= 6
        self.net.filterSubnets(subnetFilter)

        'Ensure that there is only one subnet now'
        assert self.net.countSubnets() == 1

        'Ensure that nothing intersects the vertical subnet'
        results = self.net._getSegmentIntersections(self.segmentFactory.getSegment((9, 1), (11, 1)))
        assert len(results) == 0

