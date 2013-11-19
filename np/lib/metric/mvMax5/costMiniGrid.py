'Estimate the construction and maintenance cost of a system (mini-grid)'
'Carbajal adjustments to MiniGrids to make them generic hybrids'
# Import system modules
import numpy
# Import custom modules
from np.lib.variable_store import Variable as V
from np.lib import store, metric
import finance
import demographics
import demand
import costDistribution



## Mini-grid system cost parameters ##

class DistributionLoss(V):

    section = 'system (mini-grid)'
    option = 'distribution loss'
    aliases = ['mg_loss']
    c = dict(check=store.assertLessThanOne)
    default = 0.10
    units = 'fraction'

#Nomenclature Change - available capacities 
class DieselGeneratorAvailableSystemCapacities(V):

    section = 'system (mini-grid)'
    option = 'available power generation system capacities(kW)'
    aliases = ['mg_dg_cps']
    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1000 750 500 400 200 150 100 70 32 19 12 6'
    units = 'kilowatts list'

#Nomenclature change - capital costs
class DieselGeneratorCostPerDieselSystemKilowatt(V):

    section = 'system (mini-grid)'
    option = 'power generatation cost per system kilowatt'
    aliases = ['mg_dg_ck']
    default = 150
    units = 'dollars per kilowatt'

#Nomenclature Change - percent install cost
class DieselGeneratorInstallationCostAsFractionOfGeneratorCost(V):

    section = 'system (mini-grid)'
    aliases = ['mg_dg_if']
    option = 'power generatation installation cost as fraction of generator cost'
    default = 0.50

#Nomenclature change - lifetime is still relevannt
class DieselGeneratorLifetime(V):

    section = 'system (mini-grid)'
    option = 'power generatation system lifetime'
    aliases = ['mg_dg_life']
    c = dict(check=store.assertPositive)
    default = 10
    units = 'years'

#!! big calculation change, fuel cost per L should be simplified to cost per kWh.  applies to any hybrid system now...
class DieselFuelCostPerLiter(V):

    section = 'system (mini-grid)'
    option = 'fuel or storage cost per kWh'
    aliases = ['mg_fl_cl']
    default = 0.50
    units = 'dollars per kWh'

#!! big calculation change, consider effective load percent that requires storage or fuel, more generic expression
class DieselFuelLitersConsumedPerKilowattHour(V):

    section = 'system (mini-grid)'
    option = 'percent of daily load that requires storage or fuel'
    aliases = ['mg_fl_lkwh']
    default = 0.7
    units = 'percent'

#!! big change, generator will be modeled as a factor of its capacity factor
class DieselGeneratorMinimumHoursOfOperationPerYear(V):

    section = 'system (mini-grid)'
    option = 'capacity factor of power generation as factor of actual output to nameplate output'
    aliases = ['mg_dg_mnhr']
    default = 0.90
    units = 'ratio'

#nomenclature change, generalize diesel genset to power generation 
class DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost(V):

    section = 'system (mini-grid)'
    option = 'power geratation operations and maintenance cost per year as fraction of generator cost'
    aliases = ['mg_dg_omf']
    default = 0.01


## Mini-grid system cost derivatives ##

#! big change, since now power generation system will be dictated by capacity factor 
class DieselGeneratorDesiredSystemCapacity(V):

    section = 'system (mini-grid)'
    option = 'power generation desired system capacity'
    aliases = ['mg_dg_dcp']
    dependencies = [
        demand.ProjectedPeakNodalDemand,
        DistributionLoss,
        DieselGeneratorMinimumHoursOfOperationPerYear,
        
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(demand.ProjectedPeakNodalDemand) / float(1 - self.get(DistributionLoss)) / float(self.get(DieselGeneratorMinimumHoursOfOperationPerYear))

#nomenclature change, since now power generation system will conform to given list of standards
class DieselGeneratorActualSystemCapacityCounts(V):

    section = 'system (mini-grid)'
    option = 'power generation system actual system capacity counts'
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

#nomenclature change
class DieselGeneratorActualSystemCapacity(V):

    section = 'system (mini-grid)'
    option = 'power generation actual system capacity'
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

#nomenclature change
class DieselGeneratorCost(V):

    section = 'system (mini-grid)'
    option = 'power generation system cost'
    aliases = ['mg_dg_ini']
    dependencies = [
        DieselGeneratorCostPerDieselSystemKilowatt,
        DieselGeneratorActualSystemCapacity,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(DieselGeneratorCostPerDieselSystemKilowatt) * self.get(DieselGeneratorActualSystemCapacity)

#nomenclature 
class DieselGeneratorInstallationCost(V):

    section = 'system (mini-grid)'
    option = 'power generatation installation cost'
    aliases = ['mg_dg_i']
    dependencies = [
        DieselGeneratorInstallationCostAsFractionOfGeneratorCost,
        DieselGeneratorCost,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(DieselGeneratorInstallationCostAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)

#nomenclature 
class DieselGeneratorOperationsAndMaintenanceCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'power generation operations and maintenance cost per year'
    aliases = ['mg_dg_om']
    dependencies = [
        DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost,
        DieselGeneratorCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)

#nomenclature 
class DieselGeneratorReplacementCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'power generatation lifetime replacement cost per year'
    aliases = ['mg_dg_rep']
    dependencies = [
        DieselGeneratorCost,
        DieselGeneratorLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(DieselGeneratorCost) / float(self.get(DieselGeneratorLifetime))

#this variable is not needed anymore
##class DieselGeneratorEffectiveHoursOfOperationPerYear(V):
##
##    section = 'system (mini-grid)'
##    option = 'power generation hours of operation per year (effective)'
##    aliases = ['mg_dg_efhr']
##    dependencies = [
##        demand.ProjectedNodalDemandPerYear,
##        DistributionLoss,
##        DieselGeneratorMinimumHoursOfOperationPerYear,
##        DieselGeneratorActualSystemCapacity,
##    ]
##    units = 'hours per year'
##
##    def compute(self):
##        # Initialize
##        dieselGeneratorActualSystemCapacity = self.get(DieselGeneratorActualSystemCapacity)
##        # If the capacity of the diesel generator is zero,
##        if dieselGeneratorActualSystemCapacity == 0:
##            # Return zero hours of operation
##            return 0
##        # Compute effectiveDemandPerYear and assume a mini-grid diesel generator has distribution loss
##        effectiveDemandPerYear = self.get(demand.ProjectedNodalDemandPerYear) / float(1 - self.get(DistributionLoss))
##        # Return
##        return max(self.get(DieselGeneratorMinimumHoursOfOperationPerYear), effectiveDemandPerYear / float(dieselGeneratorActualSystemCapacity))

#output generic fuel/battery cost per year based on ratio of nodal demand for which fuel/storage is needed
class DieselFuelCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'fuel and/or storage costs per year'
    aliases = ['mg_fl']
    dependencies = [
        DieselFuelCostPerLiter, #fuel or storage cost per kWh
        DieselFuelLitersConsumedPerKilowattHour, #percent of daily load that requires storage or fuel'
        #DieselGeneratorActualSystemCapacity, #Actual system capacity 
        #DieselGeneratorEffectiveHoursOfOperationPerYear,
        demand.ProjectedNodalDemandPerYear,
        DistributionLoss,
    ]
    units = 'dollars per year'


    def compute(self):
        #Initialize
        #Compute effectiveDemandPerYear and assume a mini-grid diesel generator has distribution loss
        effectiveDemandPerYear = self.get(demand.ProjectedNodalDemandPerYear) / float(1 - self.get(DistributionLoss))
        
        return self.get(DieselFuelCostPerLiter) * self.get(DieselFuelLitersConsumedPerKilowattHour) * effectiveDemandPerYear

#nomenclature change 
class MiniGridSystemNodalDiscountedDieselFuelCost(V):

    section = 'system (mini-grid)'
    option = 'system nodal discounted fuel and/or storage cost'
    aliases = ['mg_nod_ddfc']
    dependencies = [
        DieselFuelCostPerYear,
    ]

    def compute(self):
        return self.get(DieselFuelCostPerYear) * self.get(finance.DiscountedCashFlowFactor)

#nomenclature change 
class MiniGridSystemInitialDieselCost(V):

    section = 'system (mini-grid)'
    option = 'system initial power generation system cost'
    aliases = ['mg_inidc']
    dependencies = [
        DieselGeneratorCost,
        DieselGeneratorInstallationCost,
    ]
    units = 'dollars'

    def compute(self):
        return sum([
            self.get(DieselGeneratorCost),
            self.get(DieselGeneratorInstallationCost),
        ])

#nomenclature change 
class MiniGridSystemRecurringDieselCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'system recurring power generation costs per year'
    aliases = ['mg_recdc']
    dependencies = [
        DieselGeneratorOperationsAndMaintenanceCostPerYear,
        DieselGeneratorReplacementCostPerYear,
        DieselFuelCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(DieselGeneratorOperationsAndMaintenanceCostPerYear),
            self.get(DieselGeneratorReplacementCostPerYear),
            self.get(DieselFuelCostPerYear),
        ])

#nomenclature change
class MiniGridSystemNodalDiscountedDieselCost(V):

    section = 'system (mini-grid)'
    option = 'system nodal discounted power generation costs'
    aliases = ['mg_nod_ddc']
    dependencies = [
        MiniGridSystemInitialDieselCost,
        MiniGridSystemRecurringDieselCostPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(MiniGridSystemInitialDieselCost) + self.get(MiniGridSystemRecurringDieselCostPerYear) * self.get(finance.DiscountedCashFlowFactor)


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
