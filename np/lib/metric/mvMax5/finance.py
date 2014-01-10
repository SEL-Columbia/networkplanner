'Estimate finance requirements'
# Import system modules
import numpy
import math
# Import custom modules
from np.lib.variable_store import Variable as V
from np.lib import store



# Finance parameters


class TimeHorizon(V):
    
    section = 'finance'
    option = 'time horizon'
    aliases = ['time']

    short_section = 'Fin'
    short_option = 'TimeHrzn'

    c = dict(parse=store.parseCeilInteger)
    default = 10
    units = 'years'


class InterestRatePerYear(V):

    section = 'finance'
    option = 'interest rate per year'
    aliases = ['interest_g']

    short_section = 'Fin'
    short_option = 'IntRtPrYr'

    default = 0.1
    units = 'fraction per year'


class EconomicGrowthRatePerYear(V):

    section = 'finance'
    option = 'economic growth rate per year'
    aliases = ['economic_g']

    short_section = 'Fin'
    short_option = 'EconGrRtPrYr'

    default = 0.06
    units = 'fraction per year'


class ElasticityOfElectricityDemand(V):

    section = 'finance'
    option = 'elasticity of electricity demand'
    aliases = ['elasticity']

    short_section = 'Fin'
    short_option = 'ElstOfElecDmd'

    default = 1.5



# Finance derivatives


class ElectricityDemandGrowthRatePerYear(V):

    section = 'finance'
    option = 'electricity demand growth rate per year'
    aliases = ['dem_g']

    short_section = 'Fin'
    short_option = 'ElecDmdGrRtPrYr'

    dependencies = [
        ElasticityOfElectricityDemand,
        EconomicGrowthRatePerYear,
    ]
    units = 'fraction per year'

    def compute(self):
        return abs(self.get(ElasticityOfElectricityDemand)) * self.get(EconomicGrowthRatePerYear)


class ElectricityDemandMultiplier(V):

    section = 'finance'
    option = 'electricity demand multiplier'
    aliases = ['demf']

    short_section = 'Fin'
    short_option = 'ElecDmdMult'

    dependencies = [
        ElectricityDemandGrowthRatePerYear,
        TimeHorizon,
    ]

    def compute(self):
        return (1 + self.get(ElectricityDemandGrowthRatePerYear)) ** self.get(TimeHorizon)


class DiscountedCashFlowFactor(V):

    section = 'finance'
    option = 'discounted cash flow factor'
    aliases = ['dcff']

    short_section = 'Fin'
    short_option = 'DiscCshFlwFctr'

    dependencies = [
        TimeHorizon,
        InterestRatePerYear,
    ]

    def compute(self):
        interestExponents = [-x for x in xrange(1, self.get(TimeHorizon) + 1)]
        return sum(numpy.array(1 + self.get(InterestRatePerYear)) ** interestExponents)
