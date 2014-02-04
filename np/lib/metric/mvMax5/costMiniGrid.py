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
    aliases = ['mg_dist_lss', 'mg_loss']


    c = dict(check=store.assertLessThanOne)
    default = 0.10
    units = 'fraction'

#Nomenclature Change - available capacities- class name changed
class GenerationAvailableSystemCapacities(V):

    section = 'system (mini-grid)'
    option = 'available power generation system capacities(kW)'
    aliases = ['mg_avbl_gntn_sys_cap_kw', 'mg_g_cps']


    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1000 750 500 400 200 150 100 70 32 19 12 6'
    units = 'kilowatts list'

#Nomenclature change - capital costs - - class name changed
class GenerationCostPerSystemKilowatt(V):

    section = 'system (mini-grid)'
    option = 'generation cost per system kilowatt'
    aliases = ['mg_gntn_cst_pr_sys_kw', 'mg_g_ck']


    default = 150
    units = 'dollars per kilowatt'

#Nomenclature Change - percent install cost- class name changed
class GenerationInstallationCostAsFractionOfGenerationCost(V):

    section = 'system (mini-grid)'
    aliases = ['mg_gntn_inst_cst_as_fctn_of_gntn_cst', 'mg_g_if']
    option = 'generation installation cost as fraction of generation cost'


    default = 0.25
    units = 'fraction'

#Nomenclature change - lifetime is still relevannt- class name changed
class GenerationLifetime(V):

    section = 'system (mini-grid)'
    option = 'generation system lifetime'
    aliases = ['mg_gntn_sys_life', 'mg_g_life']


    c = dict(check=store.assertPositive)
    default = 5
    units = 'years'

#!! big calculation change, fuel cost per L should be simplified to cost per kWh.  applies to any hybrid system now...- class name changed
class EnergyStorageCostPerKilowattHour(V):

    section = 'system (mini-grid)'
    option = 'energy storage cost per kWh'
    aliases = ['mg_en_strg_cst_pr_kw_hr', 'mg_escpk']


    default = 0.54 #matches old defaults of $1.08/L fuel @ 0.5L/kWh fuel consumption 
    units = 'dollars per kilowatt-hour'

#!! big calculation change, consider effective load percent that requires storage or fuel, more generic expression- class name changed
class PercentOfDailyKilowattHourLoadRequiringStorage(V):

    section = 'system (mini-grid)'
    option = 'percent of daily load that requires storage or fuel'
    aliases = ['mg_pct_of_dly_kw_hr_ld_req_strg', 'mg_pd_kwhrs']


    default = 1.0 #diesel systems require 100% energy  to come via fuel, solar-batteries require near 100% storage too
    units = 'fraction'

# Introducing variable that sets floor capacity value for energy storage system
# When compared to MVMax4, this is comparable to the value of "DieselGeneratorMinimumHoursOfOperationPerYear" since we now consider
# storage requirements to encompass both fuel and battery costs
class MinimumEnergyStorageCapacity(V):

    section = 'system (mini-grid)'
    option = 'minimum size of daily capacity of energy storage system (kWh)'
    aliases = ['mg_min_strg_cap_pr_dy', 'mg_mnesc']
    default = 24
    units = 'kilowatt-hours per day'


#!! big change, generator will be modeled as a factor of its capacity factor- class name changed
class GenerationCapacityFactor(V):
#this is an inherent measurement of how efficient the generation technology is at generating power in a useful manner based on supply-side characeristics 
#<http://en.wikipedia.org/wiki/Capacity_factor>
    
    section = 'system (mini-grid)'
    option = 'capacity factor of generation as factor of nameplate output'
    aliases = ['mg_cpty_fctr_of_gntn_as_fctr_of_nmplt_cap', 'mg_g_cf']


    default = 1.0 #diesel generator has a 100% capacity factor, solar ~17% per solar hours
    units = 'fraction'

#!! big change, generator will be modeled as a factor of its utilization factor too 
class UtilizationFactor(V):
#this is an inherent measurement of how efficient the generation technology is at being utilized in a useful manner based on demand-side usage

    section = 'system (mini-grid)'
    option = 'utilization factor of power generation as factor of nameplate output'
    aliases = ['mg_utzn_fctr_pwr_gntn_fctr_nmplt_otpt', 'mg_u_fctr']


    default = 0.416667 #diesel generator has a 41.667% utilization factor
    #=> 1/[(Peak Demand as Fraction of Nodal Demand/Peak Hours Per Year)*Total Hours in Year]
    #=> 1/[ (0.40/1460hr/yr)*24 hrs/day * 365 days/yr] = 0.4166667 = 41.667%
    #Solar-battery system would be 100% because it's all dispatched on demand via electronics and fully utilized
    units = 'fraction'

    
#nomenclature change, generalize diesel genset to power generation - class name changed
class GenerationOperationsAndMaintenanceCostPerYearAsFractionOfGenerationCost(V):

    section = 'system (mini-grid)'
    option = 'generation operations and maintenance cost per year as fraction of generation cost'
    aliases = ['mg_gntn_o_and_m_cst_pr_yr_as_fctn_of_gntn_cst', 'mg_g_omf']


    default = 0.01

    units = 'fraction'

###This conversion variable can stay 'hidden' to simplify model's parameters  
##class GenerationHoursOfOperationPerYear(V):
##
##    section = 'system (mini-grid)'
##    option = 'generation hours of operation per year'
##    aliases = ['mg_gntn_hr_oprn_pr_yr', 'mg_g_sh']
##
##
##    default = float(365*24)
##    units = 'hours per year'


## Mini-grid system cost derivatives ##

#! big change, since now power generation system will be dictated by capacity factor - class name changed
class GenerationDesiredSystemCapacity(V):

    section = 'system (mini-grid)'
    option = 'generation desired system capacity'
    aliases = ['mg_gntn_dsrd_sys_cpty', 'mg_g_dcp']


    dependencies = [
        demand.ProjectedNodalDemandPerYear,
        DistributionLoss,
        GenerationCapacityFactor,
        UtilizationFactor,
        
    ]
    units = 'kilowatts'

    def compute(self):
        #Compute effectiveDemandPerYear and assume a mini-grid generator has distribution loss
        effectiveDemandPerYear = (self.get(demand.ProjectedNodalDemandPerYear) / 
                                  float(1 - self.get(DistributionLoss)))

        #Compute Service Hours per year
        GenerationHoursOfOperationPerYear = 365*24

        #Return
        return (effectiveDemandPerYear / 
                float(self.get(GenerationCapacityFactor)) / #reduce by factor of how much of nameplate power can be utilized per supply-side characteristics 
                float(self.get(UtilizationFactor)) / #derate by utilization factor of nameplate rating based on demand-side behavior
                GenerationHoursOfOperationPerYear) #factor to convert energy usage [kWh] to power [kW] sizing


#nomenclature change, since now power generation system will conform to given list of standards - class name changed
class GenerationActualSystemCapacityCounts(V):

    section = 'system (mini-grid)'
    option = 'generation actual system capacity counts'
    aliases = ['mg_gntn_sys_actl_sys_cpty_cts', 'mg_g_acps']


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

    section = 'system (mini-grid)'
    option = 'generation actual system capacity'
    aliases = ['mg_gntn_actl_sys_cpty', 'mg_g_acp']


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

    section = 'system (mini-grid)'
    option = 'low voltage line equipment cost'
    aliases = ['mg_lv_ln_eqmt_cst', 'mg_le']


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
    aliases = ['mg_lv_ln_eqmt_o_and_m_cst_pr_yr', 'mg_le_om']


    dependencies = [
        costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost,
        LowVoltageLineEquipmentCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost) * self.get(LowVoltageLineEquipmentCost)

#nomenclature change - class name changed
class GenerationCost(V):

    section = 'system (mini-grid)'
    option = 'generation system cost'
    aliases = ['mg_gntn_sys_cst', 'mg_g_ini']


    dependencies = [
        GenerationCostPerSystemKilowatt,
        GenerationActualSystemCapacity,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(GenerationCostPerSystemKilowatt) * 
                self.get(GenerationActualSystemCapacity))

#nomenclature - class name changed
class GenerationInstallationCost(V):

    section = 'system (mini-grid)'
    option = 'generation installation cost'
    aliases = ['mg_gntn_inst_cst', 'mg_g_i']


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

    section = 'system (mini-grid)'
    option = 'generation operations and maintenance cost per year'
    aliases = ['mg_gntn_o_and_m_cst_pr_yr', 'mg_g_om']


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

    section = 'system (mini-grid)'
    option = 'generation lifetime replacement cost per year'
    aliases = ['mg_gntn_life_rpmt_cst_pr_yr', 'mg_g_rep']


    dependencies = [
        GenerationCost,
        GenerationLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(GenerationCost) / float(self.get(GenerationLifetime))


# generic fuel/battery demand per year as a ratio of nodal demand for which fuel/storage is needed
class EnergyStorageDemandPerYear(V):

    section = 'system (mini-grid)'
    option = 'energy storage demand per year'
    aliases = ['mg_en_strg_dmd_pr_yr', 'mg_esdpy']

    dependencies = [
        PercentOfDailyKilowattHourLoadRequiringStorage, #percent of daily load that requires storage or fuel
        demand.ProjectedNodalDemandPerYear,
        DistributionLoss,
        MinimumEnergyStorageCapacity,
    ]
    units = 'kilowatt-hours per year'

    def compute(self):
        #Initialize
        #Compute effectiveDemandPerYear and assume a mini-grid diesel generator has distribution loss
        effectiveDemandPerYear = (self.get(demand.ProjectedNodalDemandPerYear) / 
                                  float(1 - self.get(DistributionLoss)))

        #Determine Minimum Storage System Size acceptable for minigrid
        #Don't consider energy storage systems below that value
        return max(self.get(MinimumEnergyStorageCapacity)*365,
                            effectiveDemandPerYear*float(self.get(PercentOfDailyKilowattHourLoadRequiringStorage)))


# generic fuel/battery cost per year 
class EnergyStorageCostPerYear(V):

    section = 'system (mini-grid)'
    option = 'energy storage cost per year'
    aliases = ['mg_en_strg_cst_pr_yr', 'mg_escpy']


    dependencies = [
        EnergyStorageCostPerKilowattHour, #fuel or storage cost per kWh
        EnergyStorageDemandPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
                
        return (self.get(EnergyStorageCostPerKilowattHour) * 
                self.get(EnergyStorageDemandPerYear))


#nomenclature change - class name changed
class MiniGridSystemNodalDiscountedEnergyStorageCost(V):

    section = 'system (mini-grid)'
    option = 'system nodal discounted energy storage cost'
    aliases = ['mg_sys_ndl_disc_en_strg_cst', 'mg_nod_desc']


    dependencies = [
        EnergyStorageCostPerYear,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(EnergyStorageCostPerYear) * 
                self.get(finance.DiscountedCashFlowFactor))

#nomenclature change - class name changed 
class MiniGridSystemInitialGenerationCost(V):

    section = 'system (mini-grid)'
    option = 'system initial generation system cost'
    aliases = ['mg_sys_init_gntn_cst', 'mg_ini_gc']


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

    section = 'system (mini-grid)'
    option = 'system recurring power generation cost per year'
    aliases = ['mg_sys_rcrg_gntn_cst_pr_yr', 'mg_rec_gcpy']


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

    section = 'system (mini-grid)'
    option = 'system nodal discounted generation costs'
    aliases = ['mg_sys_ndl_disc_gen_cst', 'mg_nod_dgc']


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

    section = 'system (mini-grid)'
    option = 'system initial cost'
    aliases = ['mg_sys_init_cst', 'mg_ini']


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

    section = 'system (mini-grid)'
    option = 'system recurring cost per year'
    aliases = ['mg_sys_rcrg_cst_pr_yr', 'mg_rec']


    dependencies = [
        GenerationOperationsAndMaintenanceCostPerYear,
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

    section = 'system (mini-grid)'
    option = 'system nodal discounted cost'
    aliases = ['mg_sys_ndl_disc_cst', 'mg_nod_d']


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
    aliases = ['mg_sys_ndl_lvlzd_cst', 'mg_nod_lev']


    dependencies = [
        demand.ProjectedNodalDiscountedDemand,
        MiniGridSystemNodalDiscountedCost,
    ]
    units = 'dollars per kilowatt-hour'

    def compute(self):
        if self.get(demand.ProjectedNodalDiscountedDemand) == 0:
            return 0
        return self.get(MiniGridSystemNodalDiscountedCost) / float(self.get(demand.ProjectedNodalDiscountedDemand))
