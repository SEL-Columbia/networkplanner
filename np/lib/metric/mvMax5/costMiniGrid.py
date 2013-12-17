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

    section = 'MG'
    option = 'distribution loss'
    aliases = ['mg_loss']
    c = dict(check=store.assertLessThanOne)
    default = 0.10
    units = 'fraction'

#Nomenclature Change - available capacities- class name changed
class GenerationAvailableSystemCapacities(V):

    section = 'MG'
    option = 'AvblGntnSysCapkW'
    aliases = ['mg_g_cps']
    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1000 750 500 400 200 150 100 70 32 19 12 6'
    units = 'kilowatts list'

#Nomenclature change - capital costs - - class name changed
class GenerationCostPerRatedKilowatt(V):

    section = 'MG'
    option = 'GntnCstPrNmpltRtngkW'
    aliases = ['mg_dg_ck']
    default = 150
    units = 'dollars per kilowatt'

#Nomenclature Change - percent install cost- class name changed
class GenerationInstallationCostAsFractionOfGenerationCost(V):

    section = 'MG'
    aliases = ['mg_g_if']
    option = 'GntnInstCstAsFctnOfGntnCst'
    default = 0.25
    units = 'fraction'

#Nomenclature change - lifetime is still relevannt- class name changed
class GenerationLifetime(V):

    section = 'MG'
    option = 'GntnSysLife'
    aliases = ['mg_g_life']
    c = dict(check=store.assertPositive)
    default = 5
    units = 'years'

#!! big calculation change, fuel cost per L should be simplified to cost per kWh.  applies to any hybrid system now...- class name changed
class EnergyStorageCostPerKilowattHour(V):

    section = 'MG'
    option = 'EnStrgCstPrkWHr'
    aliases = ['mg_escpk']
    default = 0.54 #matches old defaults of $1.08/L fuel @ 0.5L/kWh fuel consumption 
    units = 'dollars per kWh'

#!! big calculation change, consider effective load percent that requires storage or fuel, more generic expression- class name changed
class PercentOfDailyKilowattHourLoadRequiringStorage(V):

    section = 'MG'
    option = 'PctOfDlykWHrLdReqStrg'
    aliases = ['mg_pdkwhrs']
    default = 1.0 #diesel systems require 100% energy  to come via fuel, solar-batteries require near 100% storage too
    units = 'percent'

#!! big change, generator will be modeled as a factor of its capacity factor- class name changed
class GenerationCapacityFactor(V):

    section = 'MG'
    option = 'CptyFctrOfGntnAsFctrOfNmpltCap'
    aliases = ['mg_g_cf']
    default = 1.0 #diesel generator has a 100% capacity factor, solar ~17% per solar hours
    units = 'ratio'

#!! big change, generator will be modeled as a factor of its utilization factor too 
class GenerationUtilizationFactor(V):

    section = 'MG'
    option = 'UtlztnFctrOfGntnAsFctrOfNmpltCap'
    aliases = ['mg__g_uf']
    default = 0.10 #diesel generator has a 10% capacity factor
    #(40% of load)/(4 peak hours/day) =  0.10
    #Solar-battery system would be 100% because it's all dispatched on demand via electronics and fully utilized
    units = 'ratio'

    
#nomenclature change, generalize diesel genset to power generation - class name changed
class GenerationOperationsAndMaintenanceCostPerYearAsFractionOfGenerationCost(V):

    section = 'MG'
    option = 'GntnOandMCstPrYrAsFctnOfGntrCst'
    aliases = ['mg_g_omf']
    default = 0.01


## Mini-grid system cost derivatives ##

class GenerationDaysOfOperationPerYear(V):

    section = 'MG'
    option = 'GntnDaysOfOprnPrYr'
    aliases = ['mg_g_sd']
    default = float(365)
    units = 'days'

#! big change, since now power generation system will be dictated by capacity factor - class name changed
class GenerationDesiredSystemCapacity(V):

    section = 'MG'
    option = 'GntnDsrdSysCpty'
    aliases = ['mg_g_dcp']
    dependencies = [
        demand.ProjectedNodalDemandPerYear,
        GenerationDaysOfOperationPerYear,
        DistributionLoss,
        GenerationCapacityFactor,
        GenerationUtilizationFactor,
        
    ]
    units = 'kilowatts'

    def compute(self):
        #Compute effectiveDemandPerYear and assume a mini-grid generator has distribution loss
        effectiveDemandPerYear = (self.get(demand.ProjectedNodalDemandPerYear) / 
                                  float(1 - self.get(DistributionLoss)))
        #Return
        return (effectiveDemandPerYear / 
                float(self.get(GenerationCapacityFactor)) / #reduce by factor of how much of installed power can be utilized on average
                self.get(GenerationDaysOfOperationPerYear) * #factor to convert energy usage to power sizing
                float(self.get(GenerationUtilizationFactor))) #derate by utilization factor such as diesel system presents


#nomenclature change, since now power generation system will conform to given list of standards - class name changed
class GenerationActualSystemCapacityCounts(V):

    section = 'MG'
    option = 'GntnSysActlSysCptyCts'
    aliases = ['mg_g_acps']
    c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
    dependencies = [
        GenerationDesiredSystemCapacity,
        GenerationAvailableSystemCapacities,
    ]
    units = 'capacity count list'

    def compute(self):
        return metric.computeSystemCounts(
            self.get(GenerationDesiredSystemCapacity), 
            self.get(GenerationAvailableSystemCapacities))

#nomenclature change - class name changed
class GenerationActualSystemCapacity(V):

    section = 'MG'
    option = 'GntnActlSysCpty'
    aliases = ['mg_g_acp']
    dependencies = [
        GenerationAvailableSystemCapacities,
        GenerationActualSystemCapacityCounts,
    ]
    units = 'kilowatts'

    def compute(self):
        return numpy.dot(
            self.get(GenerationAvailableSystemCapacities), 
            self.get(GenerationActualSystemCapacityCounts))


class LowVoltageLineEquipmentCost(V):

    section = 'MG'
    option = 'LVLnEqmtCst'
    aliases = ['mg_le']
    dependencies = [
        costDistribution.LowVoltageLineEquipmentCostPerConnection,
        demand.TargetHouseholdCount,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(costDistribution.LowVoltageLineEquipmentCostPerConnection) * self.get(demand.TargetHouseholdCount)


class LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear(V):

    section = 'MG'
    option = 'LVLnEqmtOandMCstPrYr'
    aliases = ['mg_le_om']
    dependencies = [
        costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost,
        LowVoltageLineEquipmentCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost) * self.get(LowVoltageLineEquipmentCost)

#nomenclature change - class name changed
class GenerationCost(V):

    section = 'MG'
    option = 'GntnSysCst'
    aliases = ['mg_g_ini']
    dependencies = [
        GenerationCostPerRatedKilowatt,
        GenerationActualSystemCapacity,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(GenerationCostPerRatedKilowatt) * 
                self.get(GenerationActualSystemCapacity))

#nomenclature - class name changed
class GenerationInstallationCost(V):

    section = 'MG'
    option = 'GntnInstCst'
    aliases = ['mg_g_i']
    dependencies = [
        GenerationInstallationCostAsFractionOfGenerationCost,
        GenerationCost,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(GenerationInstallationCostAsFractionOfGenerationCost) * 
                self.get(GenerationCost))

#nomenclature - class name changed
class GenerationOperationsAndMaintenanceCostPerYear(V):

    section = 'MG'
    option = 'GntnOandMCstPrYr'
    aliases = ['mg_g_om']
    dependencies = [
        GenerationOperationsAndMaintenanceCostPerYearAsFractionOfGenerationCost,
        GenerationCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return (
        self.get(
        GenerationOperationsAndMaintenanceCostPerYearAsFractionOfGenerationCost) 
        * self.get(GenerationCost))

#nomenclature - class name changed
class GenerationReplacementCostPerYear(V):

    section = 'MG'
    option = 'GntnLifeRpmtCstPrYr'
    aliases = ['mg_g_rep']
    dependencies = [
        ,
        GenerationLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(GenerationCost) / float(self.get(GenerationLifetime))

"""this variable is not needed anymore
class DieselGeneratorEffectiveHoursOfOperationPerYear(V):

    section = 'MG'
    option = 'power generation hours of operation per year (effective)'
    aliases = ['mg_dg_efhr']
    dependencies = [
        demand.ProjectedNodalDemandPerYear,
        DistributionLoss,
        DieselGeneratorMinimumHoursOfOperationPerYear,
        DieselGenerationActualSystemCapacity,
    ]
    units = 'hours per year'

    def compute(self):
        # Initialize
        dieselGenerationActualSystemCapacity = self.get(DieselGenerationActualSystemCapacity)
        # If the capacity of the diesel generator is zero,
        if dieselGenerationActualSystemCapacity == 0:
            # Return zero hours of operation
            return 0
        # Compute effectiveDemandPerYear and assume a mini-grid diesel generator has distribution loss
        effectiveDemandPerYear = self.get(demand.ProjectedNodalDemandPerYear) / float(1 - self.get(DistributionLoss))
        # Return
        return max(self.get(DieselGeneratorMinimumHoursOfOperationPerYear), effectiveDemandPerYear / float(dieselGenerationActualSystemCapacity))
"""

#output generic fuel/battery cost per year based on ratio of nodal demand for which fuel/storage is needed - class name changed
class EnergyStorageCostPerYear(V):

    section = 'MG'
    option = 'EnStrgCstsPrYr'
    aliases = ['mg_escpy']
    dependencies = [
        EnergyStorageCostPerKilowattHour, #fuel or storage cost per kWh
        PercentOfDailyKilowattHourLoadRequiringStorage, #percent of daily load that requires storage or fuel'
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
        
        return (self.get(EnergyStorageCostPerKilowattHour) * 
                float(self.get(PercentOfDailyKilowattHourLoadRequiringStorage)) * 
                effectiveDemandPerYear)

#nomenclature change - class name changed
class MiniGridSystemNodalDiscountedEnergyStorageCost(V):

    section = 'MG'
    option = 'system nodal discounted fuel and/or storage cost'
    aliases = ['mg_nod_ddfc']
    dependencies = [
        EnergyStorageCostPerYear,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(EnergyStorageCostPerYear) * 
                self.get(finance.DiscountedCashFlowFactor))

#nomenclature change - class name changed 
class MiniGridSystemInitialGenerationCost(V):

    section = 'MG'
    option = 'system initial power generation system cost'
    aliases = ['mg_inidc']
    dependencies = [
        GenerationCost,
        GenerationInstallationCost,
    ]
    units = 'dollars'

    def compute(self):
        return sum([
            self.get(GenerationCost),
            self.get(GenerationInstallationCost),
        ])

#nomenclature change - class name changed 
#CN:  This was in conflict with MiniGridSystemRecurringCostPerYear
#     defined below, so I renamed it and rolled it into
#     MiniGridSystemNodalDiscountedGenerationCost
class MiniGridSystemRecurringGenerationCostPerYear(V):

    section = 'MG'
    option = 'system recurring power generation costs per year'
    aliases = ['mg_recdc']
    dependencies = [
        GenerationOperationsAndMaintenanceCostPerYear,
        GenerationReplacementCostPerYear,
        EnergyStorageCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(GenerationOperationsAndMaintenanceCostPerYear),
            self.get(GenerationReplacementCostPerYear),
            self.get(EnergyStorageCostPerYear),
        ])

#nomenclature change
class MiniGridSystemNodalDiscountedGenerationCost(V):

    section = 'MG'
    option = 'system nodal discounted power generation costs'
    aliases = ['mg_nod_ddc']
    dependencies = [
        MiniGridSystemInitialGenerationCost,
        MiniGridSystemRecurringGenerationCostPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(MiniGridSystemInitialGenerationCost) + 
                self.get(MiniGridSystemRecurringGenerationCostPerYear) * 
                self.get(finance.DiscountedCashFlowFactor))


class MiniGridSystemInitialCost(V):

    section = 'MG'
    option = 'SysInitCst'
    aliases = ['mg_ini']
    dependencies = [
        GenerationCost,
        GenerationInstallationCost,
        LowVoltageLineEquipmentCost,
        costDistribution.LowVoltageLineInitialCost,
    ]
    units = 'dollars'

    def compute(self):
        return sum([
            self.get(GenerationCost),
            self.get(GenerationInstallationCost),
            self.get(LowVoltageLineEquipmentCost),
            self.get(costDistribution.LowVoltageLineInitialCost),
        ])


class MiniGridSystemRecurringCostPerYear(V):

    section = 'MG'
    option = 'SysRcrgCstPrYr'
    aliases = ['mg_rec']
    dependencies = [
        ,
        GenerationReplacementCostPerYear,
        EnergyStorageCostPerYear,
        LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear,
        costDistribution.LowVoltageLineRecurringCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(GenerationOperationsAndMaintenanceCostPerYear),
            self.get(GenerationReplacementCostPerYear),
            self.get(EnergyStorageCostPerYear),
            self.get(LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear),
            self.get(costDistribution.LowVoltageLineRecurringCostPerYear),
        ])


class MiniGridSystemNodalDiscountedCost(V):

    section = 'MG'
    option = 'SysNdlDsctdCst'
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

    section = 'MG'
    option = 'SysNdlLvlzdCst'
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
