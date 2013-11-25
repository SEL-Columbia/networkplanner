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

#Nomenclature Change - available capacities- class name changed
class GeneratorAvailableSystemCapacities(V):

    section = 'system (mini-grid)'
    option = 'available power generation system capacities(kW)'
    aliases = ['mg_dg_cps']
    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1000 750 500 400 200 150 100 70 32 19 12 6'
    units = 'kilowatts list'

#Nomenclature change - capital costs - - class name changed
class GeneratorCostPerRatedKilowatt(V):

    section = 'system (mini-grid)'
    option = 'power generatation cost per system kilowatt'
    aliases = ['mg_dg_ck']
    default = 150
    units = 'dollars per kilowatt'

#Nomenclature Change - percent install cost- class name changed
class InstallationCostAsFractionOfGenerationCost(V):

    section = 'system (mini-grid)'
    aliases = ['mg_ic_fgc']
    option = 'power generatation installation cost as fraction of generation cost'
    default = 0.50
    units = 'fraction'

#Nomenclature change - lifetime is still relevannt- class name changed
class GeneratorLifetime(V):

    section = 'system (mini-grid)'
    option = 'power generation system lifetime'
    aliases = ['mg_dg_life']
    c = dict(check=store.assertPositive)
    default = 10
    units = 'years'

#!! big calculation change, fuel cost per L should be simplified to cost per kWh.  applies to any hybrid system now...- class name changed
class FuelCostPerKilowattHour(V):

    section = 'system (mini-grid)'
    option = 'fuel or storage cost per kWh'
    aliases = ['mg_fl_cl']
    default = 0.50
    units = 'dollars per kWh'

#!! big calculation change, consider effective load percent that requires storage or fuel, more generic expression- class name changed
class PercentOfKilowattHourRequiringFuelOrStorage(V):

    section = 'system (mini-grid)'
    option = 'percent of daily load that requires storage or fuel'
    aliases = ['mg_fl_lkwh']
    default = 0.7
    units = 'percent'

#!! big change, generator will be modeled as a factor of its capacity factor- class name changed
class CapacityFactor(V):

    section = 'system (mini-grid)'
    option = 'capacity factor of power generation as factor of nameplate output'
    aliases = ['mg_dg_mnhr']
    default = 0.90
    units = 'ratio'

#nomenclature change, generalize diesel genset to power generation - class name changed
class GeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost(V):

    section = 'system (mini-grid)'
    option = 'power geratation operations and maintenance cost per year as fraction of generator cost'
    aliases = ['mg_dg_omf']
    default = 0.01


## Mini-grid system cost derivatives ##

#! big change, since now power generation system will be dictated by capacity factor - class name changed
class GeneratorDesiredSystemCapacity(V):

    section = 'system (mini-grid)'
    option = 'power generation desired system capacity'
    aliases = ['mg_dg_dcp']
    dependencies = [
        demand.ProjectedPeakNodalDemand,
        DistributionLoss,
        CapacityFactor,
        
    ]
    units = 'kilowatts'

    #Initialize
    #Compute service hours per year in which electricity is met
    ServiceHoursPerYear = float(365*24)

    def compute(self):
        return (self.get(demand.ProjectedPeakNodalDemand) / 
                float(1 - self.get(DistributionLoss)) * 
                float(self.get(CapacityFactor)) /
                ServiceHoursPerYear)

#nomenclature change, since now power generation system will conform to given list of standards - class name changed
class GeneratorActualSystemCapacityCounts(V):

    section = 'system (mini-grid)'
    option = 'power generation system actual system capacity counts'
    aliases = ['mg_dg_acps']
    c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
    dependencies = [
        GeneratorDesiredSystemCapacity,
        GeneratorAvailableSystemCapacities,
    ]
    units = 'capacity count list'

    def compute(self):
        return metric.computeSystemCounts(
            self.get(GeneratorDesiredSystemCapacity), 
            self.get(GeneratorAvailableSystemCapacities))

#nomenclature change - class name changed
class GeneratorActualSystemCapacity(V):

    section = 'system (mini-grid)'
    option = 'power generation actual system capacity'
    aliases = ['mg_dg_acp']
    dependencies = [
        GeneratorAvailableSystemCapacities,
        GeneratorActualSystemCapacityCounts,
    ]
    units = 'kilowatts'

    def compute(self):
        return numpy.dot(
            self.get(GeneratorAvailableSystemCapacities), 
            self.get(GeneratorActualSystemCapacityCounts))


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

#nomenclature change - class name changed
class GeneratorCost(V):

    section = 'system (mini-grid)'
    option = 'power generation system cost'
    aliases = ['mg_dg_ini']
    dependencies = [
        GeneratorCostPerRatedKilowatt,
        GeneratorActualSystemCapacity,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(GeneratorCostPerRatedKilowatt) * 
                self.get(GeneratorActualSystemCapacity)

#nomenclature - class name changed
class GeneratorInstallationCost(V):

    section = 'system (mini-grid)'
    option = 'power generatation installation cost'
    aliases = ['mg_dg_i']
    dependencies = [
        InstallationCostAsFractionOfGenerationCost,
        GeneratorCost,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(InstallationCostAsFractionOfGenerationCost) * 
                self.get(GeneratorCost)

#nomenclature - class name changed
class GeneratorOperationsAndMaintenanceCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'power generation operations and maintenance cost per year'
    aliases = ['mg_dg_om']
    dependencies = [
        GeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost,
        GeneratorCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return (
        self.get(
        GeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost) 
        * self.get(GeneratorCost))

#nomenclature - class name changed
class GeneratorReplacementCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'power generatation lifetime replacement cost per year'
    aliases = ['mg_dg_rep']
    dependencies = [
        GeneratorCost,
        GeneratorLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(GeneratorCost) / float(self.get(GeneratorLifetime))

"""this variable is not needed anymore
class DieselGeneratorEffectiveHoursOfOperationPerYear(V):

    section = 'system (mini-grid)'
    option = 'power generation hours of operation per year (effective)'
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
"""

#output generic fuel/battery cost per year based on ratio of nodal demand for which fuel/storage is needed - class name changed
class FuelBatteryCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'fuel and/or storage costs per year'
    aliases = ['mg_fl']
    dependencies = [
        FuelCostPerKilowattHour, #fuel or storage cost per kWh
        PercentOfKilowattHourRequiringFuelOrStorage, #percent of daily load that requires storage or fuel'
        #DieselGeneratorActualSystemCapacity, #Actual system capacity 
        #DieselGeneratorEffectiveHoursOfOperationPerYear,
        demand.ProjectedNodalDemandPerYear,
        DistributionLoss,
    ]
    units = 'dollars per year'


    def compute(self):
        #Initialize
        #Compute effectiveDemandPerYear and assume a mini-grid diesel generator has distribution loss
        effectiveDemandPerYear = (self.get(demand.ProjectedNodalDemandPerYear) / 
                                  float(1 - self.get(DistributionLoss)))
        
        return (self.get(FuelCostPerKilowattHour) * 
                self.get(PercentOfKilowattHourRequiringFuelOrStorage) * 
                effectiveDemandPerYear)

#nomenclature change - class name changed
class MiniGridSystemNodalDiscountedFuelBatteryCost(V):

    section = 'system (mini-grid)'
    option = 'system nodal discounted fuel and/or storage cost'
    aliases = ['mg_nod_ddfc']
    dependencies = [
        FuelBatteryCostPerYear,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(FuelBatteryCostPerYear) * 
                self.get(finance.DiscountedCashFlowFactor))

#nomenclature change - class name changed 
class MiniGridSystemInitialGeneratorCost(V):

    section = 'system (mini-grid)'
    option = 'system initial power generation system cost'
    aliases = ['mg_inidc']
    dependencies = [
        GeneratorCost,
        GeneratorInstallationCost,
    ]
    units = 'dollars'

    def compute(self):
        return sum([
            self.get(GeneratorCost),
            self.get(GeneratorInstallationCost),
        ])

#nomenclature change - class name changed 
#CN:  This was in conflict with MiniGridSystemRecurringCostPerYear
#     defined below, so I renamed it and rolled it into
#     MiniGridSystemNodalDiscountedGenerationCost
class MiniGridSystemRecurringGenerationCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'system recurring power generation costs per year'
    aliases = ['mg_recdc']
    dependencies = [
        GeneratorOperationsAndMaintenanceCostPerYear,
        GeneratorReplacementCostPerYear,
        FuelBatteryCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(GeneratorOperationsAndMaintenanceCostPerYear),
            self.get(GeneratorReplacementCostPerYear),
            self.get(FuelBatteryCostPerYear),
        ])

#nomenclature change
class MiniGridSystemNodalDiscountedGenerationCost(V):

    section = 'system (mini-grid)'
    option = 'system nodal discounted power generation costs'
    aliases = ['mg_nod_ddc']
    dependencies = [
        MiniGridSystemInitialGeneratorCost,
        MiniGridSystemRecurringGenerationCostPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(MiniGridSystemInitialGeneratorCost) + 
                self.get(MiniGridSystemRecurringGenerationCostPerYear) * 
                self.get(finance.DiscountedCashFlowFactor))


class MiniGridSystemInitialCost(V):

    section = 'system (mini-grid)'
    option = 'system initial cost'
    aliases = ['mg_ini']
    dependencies = [
        GeneratorCost,
        GeneratorInstallationCost,
        LowVoltageLineEquipmentCost,
        costDistribution.LowVoltageLineInitialCost,
    ]
    units = 'dollars'

    def compute(self):
        return sum([
            self.get(GeneratorCost),
            self.get(GeneratorInstallationCost),
            self.get(LowVoltageLineEquipmentCost),
            self.get(costDistribution.LowVoltageLineInitialCost),
        ])


class MiniGridSystemRecurringCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'system recurring cost per year'
    aliases = ['mg_rec']
    dependencies = [
        GeneratorOperationsAndMaintenanceCostPerYear,
        GeneratorReplacementCostPerYear,
        FuelBatteryCostPerYear,
        LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear,
        costDistribution.LowVoltageLineRecurringCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(GeneratorOperationsAndMaintenanceCostPerYear),
            self.get(GeneratorReplacementCostPerYear),
            self.get(FuelBatteryCostPerYear),
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
        return (self.get(MiniGridSystemInitialCost) + 
                self.get(MiniGridSystemRecurringCostPerYear) * 
                self.get(finance.DiscountedCashFlowFactor))


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
