'Fit a linear or logistic curve to a series of points'
# Import system modules
import scipy.stats
import itertools
import warnings
import numpy
import math
import copy


def fit(curveType, curvePoints):
    'Fit the curve'
    # Prepare
    curvePack = curveType, curvePoints
    # If the curve has already been fitted,
    if curvePack in curveCache:
        # Return the curve
        return curveCache[curvePack]
    # Fit a new curve
    curveClass = globals()[curveType + 'Curve']
    curve = curveClass(*curvePoints)
    # Cache curve for future use
    curveCache[curvePack] = curve
    # Return curve
    return curve


def format(curve):
    'Return a string representation of the curve'
    curveType = curve.__class__.__name__.replace('Curve', '')
    curveParameters, curveXs = curve.save()
    curveYs = [curve.interpolate(x) for x in curveXs]
    return '%s %s; %s' % (curveType, ' '.join(str(x) for x in curveParameters), map(list, itertools.izip(curveXs, curveYs)))


def parse(curveString):
    'Return a curve parsed from the given string'
    curveTerms = curveString.split(';')[0].split()
    curveType = curveTerms[0]
    curveClass = globals()[curveType + 'Curve']
    return curveClass(parameters=curveTerms[1:])


class Curve(object):
    'Abstract class for fitting curves to points'

    def __init__(self, xs=None, ys=None, parameters=None):
        # If points are defined,
        if xs and ys:
            # Set
            self.xs = xs
            self.ys = ys
            # Fit
            self.fit(copy.copy(xs), copy.copy(ys))
        # If parameters are defined,
        elif parameters:
            self.load(map(float, parameters))
        # Otherwise, raise an exception
        else:
            raise SyntaxError('Please specify either points or parameters')

    def fit(self, xs, ys):
        'Fit a curve using the given coordinates'
        pass

    def interpolate(self, x):
        'Interpolate using the identity function'
        return x

    def load(self, parameters):
        pass

    def save(self):
        pass


class ZeroLinearCurve(Curve):

    def fit(self, xs, ys):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            self.gradient, self.intercept, self.rValue = scipy.stats.linregress(xs, ys)[:3]

    def interpolate(self, x):
        if x > 0:
            return self.gradient * x + self.intercept
        else:
            return 0

    def load(self, parameters):
        self.gradient, self.intercept = parameters

    def save(self):
        return (self.gradient, self.intercept), [0.1, 100]


class ZeroLogisticCurve(Curve):

    ASYMPTOTE_OFFSET = 0.01
    FAKE_COUNT = 10
    FAKE_INTERVAL = 100

    def fit(self, xs, ys):
        # Prepare
        xs, ys = list(xs), list(ys)
        self.minimumY, self.maximumY = min(ys), max(ys)
        self.minimumX, self.maximumX = min(xs), max(xs)
        # Record as floats to prevent integer rounding during division
        self.upperBound = float(self.maximumY + self.ASYMPTOTE_OFFSET)
        self.lowerBound = float(self.minimumY - self.ASYMPTOTE_OFFSET)
        # If there are too few points,
        if len(xs) < 3:
            # Add more points on the right
            xs.extend(self.maximumX + self.FAKE_INTERVAL * (i + 1) for i in xrange(self.FAKE_COUNT))
            ys.extend([self.maximumY] * self.FAKE_COUNT)
            # Add more points on the left
            xs.extend(self.minimumX - self.FAKE_INTERVAL * (i + 1) for i in xrange(self.FAKE_COUNT))
            ys.extend([self.minimumY] * self.FAKE_COUNT)
            # Sort
            xs.sort()
            ys.sort()
        # Transform points using a linearization of the logistic function
        transformedYs = [math.log(((self.upperBound / y) - 1) / (1 - (self.lowerBound / y))) for y in ys]
        # Fit a line to the transformed points
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            gradient, intercept, self.rValue, pValue, standardError = scipy.stats.linregress(xs, transformedYs)
        # Find the logistic function
        self.baseFactor = math.exp(intercept)
        self.exponentFactor = gradient

    def interpolate(self, x):
        if x > 0:
            return self.lowerBound + (self.upperBound - self.lowerBound) / float(1 + self.baseFactor * numpy.exp(self.exponentFactor * x))
        else:
            return 0

    def load(self, parameters):
        self.upperBound, self.lowerBound, self.baseFactor, self.exponentFactor, self.minimumX, self.maximumX = parameters

    def save(self):
        return (self.upperBound, self.lowerBound, self.baseFactor, self.exponentFactor, self.minimumX, self.maximumX), numpy.linspace(0.1, self.maximumX + 0.25 * (self.maximumX - self.minimumX), 100)



class ZeroLogisticLinearCurve(ZeroLogisticCurve):

    def fit(self, xs, ys):
        # Fit
        super(ZeroLogisticLinearCurve, self).fit(xs, ys)
        # Sort
        xs = sorted(xs)
        ys = sorted(ys)
        # Store relevant parameters
        self.gradient = (ys[-1] - ys[-2]) / float(xs[-1] - xs[-2])

    def interpolate(self, x):
        # If x is not positive,
        if not x > 0:
            # Return zero
            return 0
        # If x is smaller than the largest curve point,
        elif x < self.maximumX:
            # Use logistic
            return super(ZeroLogisticLinearCurve, self).interpolate(x)
        # If x is larger than or equal to the largest curve point,
        else:
            # Use linear
            return self.maximumY + self.gradient * (x - self.maximumX)

    def load(self, parameters):
        self.upperBound, self.lowerBound, self.baseFactor, self.exponentFactor, self.minimumX, self.maximumX, self.maximumY, self.gradient = parameters

    def save(self):
        return (self.upperBound, self.lowerBound, self.baseFactor, self.exponentFactor, self.minimumX, self.maximumX, self.maximumY, self.gradient), numpy.linspace(0.1, self.maximumX + 0.25 * (self.maximumX - self.minimumX), 100)



# Define

curveCache = {}
curveTypes = sorted([x.replace('Curve', '') for x in dir() if x.endswith('Curve') and x != 'Curve'])
inputCurveType = """\
<select id="${key}" name="${key}" class=value>
% for curveType in """ + str(curveTypes) + """:
    <option 
    % if value == curveType:
        selected=selected
    % endif
    >${curveType}</option>
% endfor
</select>"""
