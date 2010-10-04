"""
Julian Haimovich
Roy Hyunjin Han
"""
# Import system modules
import unittest
import shapely.geometry as g
# Import custom modules
from np.lib import network


# Vertical line at x = 0
v1 = g.LineString([(0, -1), (0, 1)])
# Vertical line at x = 1
v2 = g.LineString([(1, -1), (1, 1)])
# Vertical line at x = -2
v3 = g.LineString([(-2, -1), (-2, 1)])
# Horizontal line at y = 0
h1 = g.LineString([(1, 0), (-1, 0)])
# Horizontal line at y = -1
h2 = g.LineString([(1, -1), (-1, -1)])
# Horizontal Line at y = 1
h3 = g.LineString([(-1, 1), (1, 1)])
# Sloped line along y = x
s1 = g.LineString([(0, 0), (2, 2)])
# Sloped line along y = x starting at (1,1)
s3 = g.LineString([(1, 1), (2, 2)])
# Sloped line along y = -x
s2 = g.LineString([(0, 2) , (2, 0)])


class TestNetwork(unittest.TestCase):

    def verify(self, lines, line, category):
        m = g.MultiLineString([x.coords for x in lines])
        assert network.categorizeIntersection(m, line) == category

    def testWhenThereAreNoIntersections(self):
        # Two parallel lines do not intersect
        self.verify([v1], v2, 0)
        # Two skew line segments do not intersect    
        self.verify([v3], h1, 0)

    def testWhenThereIsOneIntersection(self):
        # Simple cross intersection
        self.verify([v1], h1, 1)
        # Intersection at endpoint
        self.verify([v1], h1, 1)
        # Interection with sloped lines
        self.verify([s1], s2, 1)

    def testWhenThereAreMultipleIntersections(self):
        # Two unique intersections between one line perpendicular to the other two
        self.verify([v1, v2], h3, 2)
        # No intersections, two parallel lines, one skew to both
        self.verify([v1, v3], s3, 0)
        # Three parallel lines
        self.verify([v1, v2], v3, 0)
        # Simple cross and endpoint intersection
        self.verify([v1, v2], s1, 2)
        # Three line segments with shared endpoint, one unique intersection
        self.verify([s3, v2], h3, 1)
