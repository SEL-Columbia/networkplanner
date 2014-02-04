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
    aliases = ['demo_pop_ct', 'pop', 'population']
    c = dict(parse=store.parseCeilInteger)
    default = 0
    units = 'person count'


class RuralPopulationGrowthRatePerYear(V):

    section = 'demographics'
    option = 'population growth rate per year (rural)'
    aliases = ['demo_pop_gr_rt_pr_yr_rur', 'pop_g_r']
    default = 0.015
    units = 'fraction per year'


class UrbanPopulationGrowthRatePerYear(V):

    section = 'demographics'
    option = 'population growth rate per year (urban)'
    aliases = ['demo_pop_gr_rt_pr_yr_urb', 'pop_g_u']
    default = 0.036
    units = 'fraction per year'


class RuralMeanHouseholdSize(V):

    section = 'demographics'
    option = 'mean household size (rural)'
    aliases = ['demo_mn_hh_sz_rur', 'ho_size_r']
    default = 9.6
    units = 'person count'


class UrbanMeanHouseholdSize(V):

    section = 'demographics'
    option = 'mean household size (urban)'
    aliases = ['demo_mn_hh_sz_urb', 'ho_size_u']
    default = 7.5
    units = 'person count'


class UrbanPopulationThreshold(V):

    section = 'demographics'
    option = 'urban population threshold'
    aliases = ['demo_urb_pop_tshd', 'u_pop_thre']
    c = dict(parse=store.parseCeilInteger)
    default = 5000
    units = 'person count'


class MeanInterhouseholdDistance(V):

    section = 'demographics'
    option = 'mean interhousehold distance'
    aliases = ['demo_mn_inter_hh_dist', 'mid']
    default = 25
    units = 'meters'


# Demographics derivatives


class ProjectedPopulationCounts(V):

    section = 'demographics'
    option = 'projected population counts'
    aliases = ['demo_prj_pop_cts', 'p_pops']
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
    aliases = ['demo_prj_pop_ct', 'p_pop']
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
    aliases = ['demo_is_rur', 'rural']
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
    aliases = ['demo_mn_hh_sz', 'ho_size']
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
    aliases = ['demo_prj_hh_ct', 'p_ho']
    c = dict(check=store.assertNonNegative)
    dependencies = [
        ProjectedPopulationCount,
        MeanHouseholdSize,
    ]
    units = 'households'

    def compute(self):
        return math.ceil(self.get(ProjectedPopulationCount) / float(self.get(MeanHouseholdSize)))
