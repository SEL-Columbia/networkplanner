'Estimate the construction and maintenance cost of a system (mini-grid)'
# Import system modules
import numpy
# Import custom modules
from np.lib.variable_store import Variable as V
from np.lib import store, metric
import finance
import demographics
import demand
import costDistribution



# Mini-grid system cost parameters


class DistributionLoss(V):

    section = 'system (mini-grid)'
    option = 'distribution loss'
    aliases = ['mg_loss']
    c = dict(check=store.assertLessThanOne)
    default = 0.10
    units = 'fraction'


class DieselGeneratorAvailableSystemCapacities(V):

    section = 'system (mini-grid)'
    option = 'available system capacities (diesel generator)'
    aliases = ['mg_dg_cps']
    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1000 750 500 400 200 150 100 70 32 19 12 6'
    units = 'kilowatts list'


class DieselGeneratorCostPerDieselSystemKilowatt(V):

    section = 'system (mini-grid)'
    option = 'diesel generator cost per diesel system kilowatt'
    aliases = ['mg_dg_ck']
    default = 150
    units = 'dollars per kilowatt'


class DieselGeneratorInstallationCostAsFractionOfGeneratorCost(V):

    section = 'system (mini-grid)'
    aliases = ['mg_dg_if']
    option = 'diesel generator installation cost as fraction of generator cost'
    default = 0.25


class DieselEquipmentCostPerConnection(V):

    section = 'system (mini-grid)'
    option = 'diesel equipment cost per connection'
    aliases = ['mg_dg_cc']
    default = 50
    units = 'dollars per connection'


class DieselGeneratorLifetime(V):

    section = 'system (mini-grid)'
    option = 'diesel generator lifetime'
    aliases = ['mg_dg_life']
    c = dict(check=store.assertPositive)
    default = 5
    units = 'years'


class DieselFuelCostPerLiter(V):

    section = 'system (mini-grid)'
    option = 'diesel fuel cost per liter'
    aliases = ['mg_fl_cl']
    default = 1.08
    units = 'dollars per liter'


class DieselFuelLitersConsumedPerKilowattHour(V):

    section = 'system (mini-grid)'
    option = 'diesel fuel liters consumed per kilowatt-hour'
    aliases = ['mg_fl_lkwh']
    default = 0.5
    units = 'liters per kilowatt-hour'


class DieselGeneratorHoursOfOperationPerYear(V):

    section = 'system (mini-grid)'
    option = 'diesel generator hours of operation per year'
    aliases = ['mg_dg_hr']
    default = 2500
    units = 'hours per year'


class DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost(V):

    section = 'system (mini-grid)'
    option = 'diesel generator operations and maintenance cost per year as fraction of generator cost'
    aliases = ['mg_dg_omf']
    default = 0.01


class DieselEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost(V):

    section = 'system (mini-grid)'
    option = 'diesel equipment operations and maintenance cost per year as fraction of equipment cost'
    aliases = ['mg_de_omf']
    default = 0.0024



# Mini-grid system cost derivatives


class DieselGeneratorDesiredSystemCapacity(V):

    section = 'system (mini-grid)'
    option = 'diesel generator desired system capacity'
    aliases = ['mg_dg_dcp']
    dependencies = [
        demand.ProjectedPeakNodalDemand,
        DistributionLoss,
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(demand.ProjectedPeakNodalDemand) / float(1 - self.get(DistributionLoss))


class DieselGeneratorActualSystemCapacityCounts(V):

    section = 'system (mini-grid)'
    option = 'diesel generator actual system capacity counts'
    aliases = ['mg_dg_acps']
    c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
    dependencies = [
        DieselGeneratorDesiredSystemCapacity,
        DieselGeneratorAvailableSystemCapacities,
    ]
    units = 'capacity count list'

    def compute(self):
        return metric.computeSystemCounts(
            self.get(DieselGeneratorDesiredSystemCapacity), 
            self.get(DieselGeneratorAvailableSystemCapacities))


class DieselGeneratorActualSystemCapacity(V):

    section = 'system (mini-grid)'
    option = 'diesel generator actual system capacity'
    aliases = ['mg_dg_acp']
    dependencies = [
        DieselGeneratorAvailableSystemCapacities,
        DieselGeneratorActualSystemCapacityCounts,
    ]
    units = 'kilowatts'

    def compute(self):
        return numpy.dot(
            self.get(DieselGeneratorAvailableSystemCapacities), 
            self.get(DieselGeneratorActualSystemCapacityCounts))


class DieselEquipmentCost(V):

    section = 'system (mini-grid)'
    option = 'diesel equipment cost'
    aliases = ['mg_de_ini']
    dependencies = [
        DieselEquipmentCostPerConnection,
        demographics.ProjectedHouseholdCount,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(DieselEquipmentCostPerConnection) * self.get(demographics.ProjectedHouseholdCount)


class DieselEquipmentOperationsAndMaintenanceCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'diesel equipment operations and maintenance cost per year'
    aliases = ['mg_de_om']
    dependencies = [
        DieselEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost,
        DieselEquipmentCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(DieselEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost) * self.get(DieselEquipmentCost)


class DieselGeneratorCost(V):

    section = 'system (mini-grid)'
    option = 'diesel generator cost'
    aliases = ['mg_dg_ini']
    dependencies = [
        DieselGeneratorCostPerDieselSystemKilowatt,
        DieselGeneratorActualSystemCapacity,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(DieselGeneratorCostPerDieselSystemKilowatt) * self.get(DieselGeneratorActualSystemCapacity)


class DieselGeneratorInstallationCost(V):

    section = 'system (mini-grid)'
    option = 'diesel generator installation cost'
    aliases = ['mg_dg_i']
    dependencies = [
        DieselGeneratorInstallationCostAsFractionOfGeneratorCost,
        DieselGeneratorCost,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(DieselGeneratorInstallationCostAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)


class DieselGeneratorOperationsAndMaintenanceCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'diesel generator operations and maintenance cost per year'
    aliases = ['mg_dg_om']
    dependencies = [
        DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost,
        DieselGeneratorCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)


class DieselGeneratorReplacementCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'diesel generator replacement cost per year'
    aliases = ['mg_dg_rep']
    dependencies = [
        DieselGeneratorCost,
        DieselGeneratorLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(DieselGeneratorCost) / float(self.get(DieselGeneratorLifetime))


class DieselFuelCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'diesel fuel cost per year'
    aliases = ['mg_fl']
    dependencies = [
        DieselFuelCostPerLiter,
        DieselFuelLitersConsumedPerKilowattHour,
        DieselGeneratorActualSystemCapacity,
        DieselGeneratorHoursOfOperationPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(DieselFuelCostPerLiter) * self.get(DieselFuelLitersConsumedPerKilowattHour) * self.get(DieselGeneratorActualSystemCapacity) * self.get(DieselGeneratorHoursOfOperationPerYear)


class MiniGridSystemInitialCost(V):

    section = 'system (mini-grid)'
    option = 'system initial cost'
    aliases = ['mg_ini']
    dependencies = [
        DieselGeneratorCost,
        DieselGeneratorInstallationCost,
        DieselEquipmentCost,
        costDistribution.LowVoltageLineInitialCost,
    ]
    units = 'dollars'

    def compute(self):
        return sum([
            self.get(DieselGeneratorCost),
            self.get(DieselGeneratorInstallationCost),
            self.get(DieselEquipmentCost),
            self.get(costDistribution.LowVoltageLineInitialCost),
        ])


class MiniGridSystemRecurringCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'system recurring cost per year'
    aliases = ['mg_rec']
    dependencies = [
        DieselGeneratorOperationsAndMaintenanceCostPerYear,
        DieselEquipmentOperationsAndMaintenanceCostPerYear,
        DieselGeneratorReplacementCostPerYear,
        DieselFuelCostPerYear,
        costDistribution.LowVoltageLineRecurringCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(DieselGeneratorOperationsAndMaintenanceCostPerYear),
            self.get(DieselEquipmentOperationsAndMaintenanceCostPerYear),
            self.get(DieselGeneratorReplacementCostPerYear),
            self.get(DieselFuelCostPerYear),
            self.get(costDistribution.LowVoltageLineRecurringCostPerYear),
        ])


class MiniGridSystemNodalDiscountedCost(V):

    section = 'system (mini-grid)'
    option = 'system nodal discounted cost'
    aliases = ['mg_nod_d']
    dependencies = [
        demand.ProjectedNodalDemandPerYear,
        MiniGridSystemInitialCost,
        MiniGridSystemRecurringCostPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'dollars'

    def compute(self):
        if self.get(demand.ProjectedNodalDemandPerYear) == 0:
            return 0
        return self.get(MiniGridSystemInitialCost) + self.get(MiniGridSystemRecurringCostPerYear) * self.get(finance.DiscountedCashFlowFactor)


class MiniGridSystemNodalLevelizedCost(V):

    section = 'system (mini-grid)'
    option = 'system nodal levelized cost'
    aliases = ['mg_nod_lev']
    dependencies = [
        demand.ProjectedNodalDiscountedDemand,
        MiniGridSystemNodalDiscountedCost,
    ]
    units = 'dollars per kilowatt-hour'

    def compute(self):
        if self.get(demand.ProjectedNodalDiscountedDemand) == 0:
            return 0
        return self.get(MiniGridSystemNodalDiscountedCost) / float(self.get(demand.ProjectedNodalDiscountedDemand))
