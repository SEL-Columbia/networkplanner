'Project demographic growth'
# Import system modules
import math
# Import custom modules
from np.lib.variable_store import Variable as V
from np.lib import store
import finance



# Demographics parameters


class PopulationCount(V):

    section = 'demographics'
    option = 'population count'
    aliases = ['Demo_PopCt', 'pop', 'population']

    short_section = 'Demo'
    short_option = 'PopCt'

    c = dict(parse=store.parseCeilInteger)
    default = 0
    units = 'person count'


class RuralPopulationGrowthRatePerYear(V):

    section = 'demographics'
    option = 'population growth rate per year (rural)'
    aliases = ['Demo_PopGrRtPrYrRur', 'pop_g_r']

    short_section = 'Demo'
    short_option = 'PopGrRtPrYrRur'

    default = 0.015
    units = 'fraction per year'


class UrbanPopulationGrowthRatePerYear(V):

    section = 'demographics'
    option = 'population growth rate per year (urban)'
    aliases = ['Demo_PopGrRtPrYrUrb', 'pop_g_u']

    short_section = 'Demo'
    short_option = 'PopGrRtPrYrUrb'

    default = 0.036
    units = 'fraction per year'


class RuralMeanHouseholdSize(V):

    section = 'demographics'
    option = 'mean household size (rural)'
    aliases = ['Demo_MnHHSzRur', 'ho_size_r']

    short_section = 'Demo'
    short_option = 'MnHHSzRur'

    default = 9.6
    units = 'person count'


class UrbanMeanHouseholdSize(V):

    section = 'demographics'
    option = 'mean household size (urban)'
    aliases = ['Demo_MnHHSzUrb', 'ho_size_u']

    short_section = 'Demo'
    short_option = 'MnHHSzUrb'

    default = 7.5
    units = 'person count'


class UrbanPopulationThreshold(V):

    section = 'demographics'
    option = 'urban population threshold'
    aliases = ['Demo_UrbPopTshd', 'u_pop_thre']

    short_section = 'Demo'
    short_option = 'UrbPopTshd'

    c = dict(parse=store.parseCeilInteger)
    default = 5000
    units = 'person count'


class MeanInterhouseholdDistance(V):

    section = 'demographics'
    option = 'mean interhousehold distance'
    aliases = ['Demo_MnInterHHDist', 'mid']

    short_section = 'Demo'
    short_option = 'MnInterHHDist'

    default = 25
    units = 'meters'


# Demographics derivatives


class ProjectedPopulationCounts(V):

    section = 'demographics'
    option = 'projected population counts'
    aliases = ['Demo_PrjPopCts', 'p_pops']

    short_section = 'Demo'
    short_option = 'PrjPopCts'

    c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
    dependencies = [
        PopulationCount,
        RuralPopulationGrowthRatePerYear,
        UrbanPopulationGrowthRatePerYear,
        UrbanPopulationThreshold,
        finance.TimeHorizon,
    ]
    units = 'person count list'

    def compute(self):
        # Initialize
        populationCounts = [self.get(PopulationCount)]
        urbanThreshold = self.get(UrbanPopulationThreshold)
        ruralGrowthRate = self.get(RuralPopulationGrowthRatePerYear)
        urbanGrowthRate = self.get(UrbanPopulationGrowthRatePerYear)
        # For each year of the time horizon,
        for year in xrange(self.get(finance.TimeHorizon)):
            # Get population count
            populationCount = populationCounts[-1]
            # Get appropriate growth rate
            populationGrowthRate = ruralGrowthRate if populationCount < urbanThreshold else urbanGrowthRate
            # Append projected population count
            populationCounts.append(int(math.ceil(populationCount * (1 + populationGrowthRate))))
        # Return
        return populationCounts


class ProjectedPopulationCount(V):

    section = 'demographics'
    option = 'projected population count'
    aliases = ['Demo_PrjPopCt', 'p_pop']

    short_section = 'Demo'
    short_option = 'PrjPopCt'

    c = dict(parse=store.parseCeilInteger)
    dependencies = [
        ProjectedPopulationCounts,
    ]
    units = 'person count'

    def compute(self):
        return self.get(ProjectedPopulationCounts)[-1]


class IsRural(V):

    section = 'demographics'
    option = 'is rural'
    aliases = ['Demo_IsRur', 'rural']

    short_section = 'Demo'
    short_option = 'IsRur'

    c = dict(parse=int)
    dependencies = [
        ProjectedPopulationCount,
        UrbanPopulationThreshold,
    ]
    units = 'binary'

    def compute(self):
        return 1 if self.get(ProjectedPopulationCount) < self.get(UrbanPopulationThreshold) else 0


class MeanHouseholdSize(V):

    section = 'demographics'
    option = 'mean household size'
    aliases = ['Demo_MnHHSz', 'ho_size']

    short_section = 'Demo'
    short_option = 'MnHHSz'

    c = dict(check=store.assertPositive)
    dependencies = [
        RuralMeanHouseholdSize,
        IsRural,
        UrbanMeanHouseholdSize,
    ]
    units = 'person count'

    def compute(self):
        return self.get(RuralMeanHouseholdSize) if self.get(IsRural) else self.get(UrbanMeanHouseholdSize)


class ProjectedHouseholdCount(V):

    section = 'demographics'
    option = 'projected household count'
    aliases = ['Demo_PrjHHCt', 'p_ho']

    short_section = 'Demo'
    short_option = 'PrjHHCt'

    c = dict(check=store.assertNonNegative)
    dependencies = [
        ProjectedPopulationCount,
        MeanHouseholdSize,
    ]
    units = 'household count'

    def compute(self):
        return math.ceil(self.get(ProjectedPopulationCount) / float(self.get(MeanHouseholdSize)))
