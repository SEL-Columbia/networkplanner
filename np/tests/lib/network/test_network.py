# Import system modules
import unittest
# Import custom modules
from np.lib import network


class TestNetwork(unittest.TestCase):

    def setUp(self):
        # Initialize
        self.net = network.Network(network.SegmentFactory(), '+proj=utm +zone=28 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')

    def verify(self, subnetCount, segmentCount):
        print '%s subnets, %s segments' % (self.net.countSubnets(), self.net.countSegments())
        assert self.net.countSubnets() == subnetCount
        assert self.net.countSegments() == segmentCount

    def testThatPlacingTwoNonOverlappingSegmentsMakesTwoSubnets(self):
        'If we have two segments that do not overlap each other, then the network should have two subnetworks.'
        # Add first segment
        self.net.addSegmentViaCoordinates((0, 1), (1, 0))
        self.verify(subnetCount=1, segmentCount=1)
        # Add second segment
        self.net.addSegmentViaCoordinates((2, 0), (3, 1))
        self.verify(subnetCount=2, segmentCount=2)

    def testThatConnectingTwoNonOverlappingSegmentsWithAThirdSegmentMakesOneSubnet(self):
        'If we have two non-overlapping segments and we connect them using a third segment, then the network should have one subnetwork.'
        # Add first segment
        self.net.addSegmentViaCoordinates((0, 1), (1, 0))
        self.verify(subnetCount=1, segmentCount=1)
        # Add second segment
        self.net.addSegmentViaCoordinates((2, 0), (3, 1))
        self.verify(subnetCount=2, segmentCount=2)
        # Add third segment
        self.net.addSegmentViaCoordinates((1, 0), (2, 0))
        self.verify(subnetCount=1, segmentCount=3)
    
    def testThatAddingTheSameSegmentTwiceDoesNotChangeTheSubnet(self):
        'If we add the same segment twice, then the subnet should be the same as though we had added the segment only once.'
        # Add first segment
        self.net.addSegmentViaCoordinates((0, 1), (1, 0))
        self.verify(subnetCount=1, segmentCount=1)
        # Add second segment
        self.net.addSegmentViaCoordinates((1, 0), (2, 0))
        self.verify(subnetCount=1, segmentCount=2)
        # Add third segment
        self.net.addSegmentViaCoordinates((1, 0), (2, 0))
        self.verify(subnetCount=1, segmentCount=2)

    def testThatAddingTwoOverlappingSegmentsMakesOneSubnet(self):
        'If we add two segments that overlap, then there should be only one subnet consisting of the larger segment.'
        # Add first segment
        self.net.addSegmentViaCoordinates((1, 0), (2, 0))
        self.verify(subnetCount=1, segmentCount=1)
        # Add second segment
        self.net.addSegmentViaCoordinates((0, 0), (3, 0))
        self.verify(subnetCount=1, segmentCount=1)

    def testThatAddingTwoIntersectingSegmentsMakesOneSubnet(self):
        'If we add two segments that intersect, then there should be only one subnet consisting of both segments.'
        # Add first segment
        self.net.addSegmentViaCoordinates((-1, 0), (1, 0))
        self.verify(subnetCount=1, segmentCount=1)
        # Add second segment
        self.net.addSegmentViaCoordinates((0, -1), (0, 1))
        self.verify(subnetCount=1, segmentCount=2)

    def testThatConnectingTwoSegmentsFromTheSameSubnetDoesNotChangeSubnet(self):
        # Add first segment
        self.net.addSegmentViaCoordinates((0, 1), (1, 0))
        self.verify(subnetCount=1, segmentCount=1)
        # Add second segment
        self.net.addSegmentViaCoordinates((1, 0), (2, 0))
        self.verify(subnetCount=1, segmentCount=2)
        # Add third segment
        self.net.addSegmentViaCoordinates((0, 1), (2, 0))
        self.verify(subnetCount=1, segmentCount=2)


if __name__ == '__main__':
    unittest.main()
