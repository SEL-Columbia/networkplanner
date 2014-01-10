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
    aliases = ['di_ll_cm']

    short_section = 'Dist'
    short_option = 'LVLnCstPrM'

    default = 10
    units = 'dollars per meter'


class LowVoltageLineLifetime(V):

    section = 'distribution'
    option = 'low voltage line lifetime'
    aliases = ['di_ll_life']

    short_section = 'Dist'
    short_option = 'LVLnLife'

    c = dict(check=store.assertPositive)
    default = 10
    units = 'years'


class LowVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost(V):

    section = 'distribution'
    option = 'low voltage line operations and maintenance cost per year as fraction of line cost'
    aliases = ['di_ll_omf']

    short_section = 'Dist'
    short_option = 'LVLnOandMCstPrYrAsFctnOfLnCst'

    default = 0.01


class LowVoltageLineEquipmentCostPerConnection(V):

    section = 'distribution'
    option = 'low voltage line equipment cost per connection'
    aliases = ['di_le_cc']

    short_section = 'Dist'
    short_option = 'LVLnEqmtCstPrConn'

    default = 200
    units = 'dollars per connection'


class LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost(V):

    section = 'distribution'
    option = 'low voltage line equipment operations and maintenance cost as fraction of equipment cost'
    aliases = ['di_le_omf']

    short_section = 'Dist'
    short_option = 'LVLnEqmtOandMCstAsFctnOfEqmtCst'

    default = 0.01


# Low voltage distribution cost derivatives


class LowVoltageLineLength(V):

    section = 'distribution'
    option = 'low voltage line length'
    aliases = ['di_ll_len']

    short_section = 'Dist'
    short_option = 'LVLnLgth'

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
    aliases = ['di_ll_ini']

    short_section = 'Dist'
    short_option = 'LVLnInitCst'

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
    aliases = ['di_ll_om']

    short_section = 'Dist'
    short_option = 'LVLnOandMCstPrYr'

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
    aliases = ['di_ll_rep']

    short_section = 'Dist'
    short_option = 'LVLnRpmtCstPrYr'

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
    aliases = ['di_ll_rec']

    short_section = 'Dist'
    short_option = 'LVLnRcrgCstPrYr'

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
