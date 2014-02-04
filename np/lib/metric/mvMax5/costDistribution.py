'Estimate the construction and maintenance cost of a low voltage distribution system'
# Import custom modules
from np.lib.variable_store import Variable as V
from np.lib import store
import demographics
import demand



# Low voltage distribution cost parameters


class LowVoltageLineCostPerMeter(V):

    section = 'distribution'
    option = 'low voltage line cost per meter'
    aliases = ['dist_lv_ln_cst_pr_m', 'di_ll_cm']


    default = 10
    units = 'dollars per meter'


class LowVoltageLineLifetime(V):

    section = 'distribution'
    option = 'low voltage line lifetime'
    aliases = ['dist_lv_ln_life', 'di_ll_life']


    c = dict(check=store.assertPositive)
    default = 10
    units = 'years'


class LowVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost(V):

    section = 'distribution'
    option = 'low voltage line operations and maintenance cost per year as fraction of line cost'
    aliases = ['dist_lv_ln_o_and_m_cst_pr_yr_as_fctn_of_ln_cst', 'di_ll_omf']


    default = 0.01


class LowVoltageLineEquipmentCostPerConnection(V):

    section = 'distribution'
    option = 'low voltage line equipment cost per connection'
    aliases = ['dist_lv_ln_eqmt_cst_pr_conn', 'di_le_cc']


    default = 200
    units = 'dollars per connection'


class LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost(V):

    section = 'distribution'
    option = 'low voltage line equipment operations and maintenance cost as fraction of equipment cost'
    aliases = ['dist_lv_ln_eqmt_o_and_m_cst_as_fctn_of_eqmt_cst', 'di_le_omf']


    default = 0.01


# Low voltage distribution cost derivatives


class LowVoltageLineLength(V):

    section = 'distribution'
    option = 'low voltage line length'
    aliases = ['dist_lv_ln_lgth', 'di_ll_len']


    dependencies = [
        demographics.MeanInterhouseholdDistance,
        demand.TargetHouseholdCount,
    ]
    units = 'meters'

    def compute(self):
        # Load
        meanInterhouseholdDistance = self.get(demographics.MeanInterhouseholdDistance)
        targetHouseholdCount = self.get(demand.TargetHouseholdCount)
        # Return
        return meanInterhouseholdDistance * (targetHouseholdCount - 1) if targetHouseholdCount > 1 else 0


class LowVoltageLineInitialCost(V):

    section = 'distribution'
    option = 'low voltage line initial cost'
    aliases = ['dist_lv_ln_init_cst', 'di_ll_ini']


    dependencies = [
        LowVoltageLineLength,
        LowVoltageLineCostPerMeter,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(LowVoltageLineCostPerMeter) * self.get(LowVoltageLineLength)


class LowVoltageLineOperationsAndMaintenanceCostPerYear(V):

    section = 'distribution'
    option = 'low voltage line operations and maintenance cost per year'
    aliases = ['dist_lv_ln_o_and_m_cst_pr_yr', 'di_ll_om']


    dependencies = [
        LowVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost,
        LowVoltageLineCostPerMeter,
        LowVoltageLineLength,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(LowVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost) * self.get(LowVoltageLineCostPerMeter) * self.get(LowVoltageLineLength)


class LowVoltageLineReplacementCostPerYear(V):

    section = 'distribution'
    option = 'low voltage line replacement cost per year'
    aliases = ['dist_lv_ln_rpmt_cst_pr_yr', 'di_ll_rep']


    dependencies = [
        LowVoltageLineInitialCost,
        LowVoltageLineLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(LowVoltageLineInitialCost) / float(self.get(LowVoltageLineLifetime))


class LowVoltageLineRecurringCostPerYear(V):

    section = 'distribution'
    option = 'low voltage line recurring cost per year'
    aliases = ['dist_lv_ln_rcrg_cst_pr_yr', 'di_ll_rec']


    dependencies = [
        LowVoltageLineOperationsAndMaintenanceCostPerYear,
        LowVoltageLineReplacementCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(LowVoltageLineOperationsAndMaintenanceCostPerYear),
            self.get(LowVoltageLineReplacementCostPerYear),
        ])
