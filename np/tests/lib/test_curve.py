'Make sure that we can fit curves properly'
# Import system modules
import unittest
# Import custom modules
from np.lib import curve


class TestCurve(unittest.TestCase):
    'Test curve functions'

    def test_curveCache(self):
        'Ensure that curve caching works properly'
        # Prepare simple curve settings
        curvePack1 = 'ZeroLinear', ((0, 1), (1, 1))
        curvePack2 = 'ZeroLogistic', ((0, 1), (1, 1))
        # Fit curves
        c1 = curve.fit(*curvePack1)
        c2 = curve.fit(*curvePack2)
        c3 = curve.fit(*curvePack1)
        # Make sure that we are getting the same exact curve
        self.assertNotEqual(id(c1), id(c2))
        self.assertEqual(id(c1), id(c3))
