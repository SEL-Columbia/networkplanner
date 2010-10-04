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


class DieselGeneratorMinimumHoursOfOperationPerYear(V):

    section = 'system (mini-grid)'
    option = 'diesel generator hours of operation per year (minimum)'
    aliases = ['mg_dg_mnhr']
    default = 1460
    units = 'hours per year'


class DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost(V):

    section = 'system (mini-grid)'
    option = 'diesel generator operations and maintenance cost per year as fraction of generator cost'
    aliases = ['mg_dg_omf']
    default = 0.01


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


class LowVoltageLineEquipmentCost(V):

    section = 'system (mini-grid)'
    option = 'low voltage line equipment cost'
    aliases = ['mg_le']
    dependencies = [
        costDistribution.LowVoltageLineEquipmentCostPerConnection,
        demand.TargetHouseholdCount,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(costDistribution.LowVoltageLineEquipmentCostPerConnection) * self.get(demand.TargetHouseholdCount)


class LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'low voltage line equipment operations and maintenance cost per year'
    aliases = ['mg_le_om']
    dependencies = [
        costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost,
        LowVoltageLineEquipmentCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost) * self.get(LowVoltageLineEquipmentCost)


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


class DieselGeneratorEffectiveHoursOfOperationPerYear(V):

    section = 'system (mini-grid)'
    option = 'diesel generator hours of operation per year (effective)'
    aliases = ['mg_dg_efhr']
    dependencies = [
        demand.ProjectedNodalDemandPerYear,
        DistributionLoss,
        DieselGeneratorMinimumHoursOfOperationPerYear,
        DieselGeneratorActualSystemCapacity,
    ]
    units = 'hours per year'

    def compute(self):
        # Initialize
        dieselGeneratorActualSystemCapacity = self.get(DieselGeneratorActualSystemCapacity)
        # If the capacity of the diesel generator is zero,
        if dieselGeneratorActualSystemCapacity == 0:
            # Return zero hours of operation
            return 0
        # Compute effectiveDemandPerYear and assume a mini-grid diesel generator has distribution loss
        effectiveDemandPerYear = self.get(demand.ProjectedNodalDemandPerYear) / float(1 - self.get(DistributionLoss))
        # Return
        return max(self.get(DieselGeneratorMinimumHoursOfOperationPerYear), effectiveDemandPerYear / float(dieselGeneratorActualSystemCapacity))


class DieselFuelCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'diesel fuel cost per year'
    aliases = ['mg_fl']
    dependencies = [
        DieselFuelCostPerLiter,
        DieselFuelLitersConsumedPerKilowattHour,
        DieselGeneratorActualSystemCapacity,
        DieselGeneratorEffectiveHoursOfOperationPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(DieselFuelCostPerLiter) * self.get(DieselFuelLitersConsumedPerKilowattHour) * self.get(DieselGeneratorActualSystemCapacity) * self.get(DieselGeneratorEffectiveHoursOfOperationPerYear)


class MiniGridSystemInitialCost(V):

    section = 'system (mini-grid)'
    option = 'system initial cost'
    aliases = ['mg_ini']
    dependencies = [
        DieselGeneratorCost,
        DieselGeneratorInstallationCost,
        LowVoltageLineEquipmentCost,
        costDistribution.LowVoltageLineInitialCost,
    ]
    units = 'dollars'

    def compute(self):
        return sum([
            self.get(DieselGeneratorCost),
            self.get(DieselGeneratorInstallationCost),
            self.get(LowVoltageLineEquipmentCost),
            self.get(costDistribution.LowVoltageLineInitialCost),
        ])


class MiniGridSystemRecurringCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'system recurring cost per year'
    aliases = ['mg_rec']
    dependencies = [
        DieselGeneratorOperationsAndMaintenanceCostPerYear,
        DieselGeneratorReplacementCostPerYear,
        DieselFuelCostPerYear,
        LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear,
        costDistribution.LowVoltageLineRecurringCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(DieselGeneratorOperationsAndMaintenanceCostPerYear),
            self.get(DieselGeneratorReplacementCostPerYear),
            self.get(DieselFuelCostPerYear),
            self.get(LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear),
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
