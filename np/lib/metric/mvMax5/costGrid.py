'Estimate the construction and maintenance cost of a grid system'
# Import system modules
import numpy
# Import custom modules
from np.lib.variable_store import Variable as V
from np.lib import store, metric
import finance
import demographics
import demand
import costDistribution



# Grid system cost parameters


class DistributionLoss(V):

    section = 'system (grid)'
    option = 'distribution loss'
    aliases = ['GR_DistLss', 'gr_loss']

    short_section = 'GR'
    short_option = 'DistLss'

    c = dict(check=store.assertLessThanOne)
    default = 0.15
    units = 'fraction'


class GridElectricityCostPerKilowattHour(V):

    section = 'system (grid)'
    option = 'electricity cost per kilowatt-hour'
    aliases = ['GR_ElecCstPrkWHr', 'gr_el_ckwh']

    short_section = 'GR'
    short_option = 'ElecCstPrkWHr'

    default = 0.17
    units = 'dollars per kilowatt-hour'


class GridTransformerAvailableSystemCapacities(V):

    section = 'system (grid)'
    option = 'available system capacities (transformer)'
    aliases = ['GR_AvblSysCapTfmr', 'gr_tr_cps']

    short_section = 'GR'
    short_option = 'AvblSysCapTfmr'

    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1000 900 800 700 600 500 400 300 200 100 90 80 70 60 50 40 30 20 15 5'
    units = 'kilowatts list'


class GridTransformerCostPerGridSystemKilowatt(V):

    section = 'system (grid)'
    option = 'transformer cost per grid system kilowatt'
    aliases = ['GR_TfmrCstPrGRSyskW', 'gr_tr_ckw']

    short_section = 'GR'
    short_option = 'TfmrCstPrGRSyskW'

    default = 1000
    units = 'dollars per kilowatt'

    
class GridTransformerLifetime(V):

    section = 'system (grid)'
    option = 'transformer lifetime'
    aliases = ['GR_TfmrLife', 'gr_tr_life']

    short_section = 'GR'
    short_option = 'TfmrLife'

    c = dict(check=store.assertPositive)
    default = 10
    units = 'years'


class GridTransformerOperationsAndMaintenanceCostPerYearAsFractionOfTransformerCost(V):

    section = 'system (grid)'
    option = 'transformer operations and maintenance cost per year as fraction of transformer cost'
    aliases = ['GR_TfmrOandMCstPrYrAsFctnOfTfmrCst', 'gr_tr_omf']

    short_section = 'GR'
    short_option = 'TfmrOandMCstPrYrAsFctnOfTfmrCst'

    default = 0.03


class GridInstallationCostPerConnection(V):

    section = 'system (grid)'
    option = 'installation cost per connection'
    aliases = ['GR_InstCstPrConn', 'gr_i_cc']

    short_section = 'GR'
    short_option = 'InstCstPrConn'

    default = 130
    units = 'dollars per connection'


class GridMediumVoltageLineCostPerMeter(V):

    section = 'system (grid)'
    option = 'medium voltage line cost per meter'
    aliases = ['GR_MVLnCstPrM', 'gr_ml_cm']

    short_section = 'GR'
    short_option = 'MVLnCstPrM'

    default = 20
    units = 'dollars per meter'


class GridMediumVoltageLineLifetime(V):

    section = 'system (grid)'
    option = 'medium voltage line lifetime'
    aliases = ['GR_MVLnLife', 'gr_ml_life']

    short_section = 'GR'
    short_option = 'MVLnLife'

    c = dict(check=store.assertPositive)
    default = 30
    units = 'years'


class GridMediumVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost(V):

    section = 'system (grid)'
    option = 'medium voltage line operations and maintenance cost per year as fraction of line cost'
    aliases = ['GR_MVLnOandMCstPrYrAsFctnOfLnCst', 'gr_ml_omf']

    short_section = 'GR'
    short_option = 'MVLnOandMCstPrYrAsFctnOfLnCst'

    default = 0.01



# Grid system cost derivatives


class GridSocialInfrastructureCount(V):
    
    section = 'system (grid)'
    option = 'social infrastructure count'
    aliases = ['GR_SoclnfCt', 'gr_so']

    short_section = 'GR'
    short_option = 'SoclnfCt'

    dependencies = [
        demand.ProjectedHealthFacilityCount,
        demand.ProjectedEducationFacilityCount,
        demand.ProjectedPublicLightingFacilityCount,
        demand.ProjectedCommercialFacilityCount,
    ]
    units = 'facility count'
   
    def compute(self):
        return self.get(demand.ProjectedHealthFacilityCount) + self.get(demand.ProjectedEducationFacilityCount) + self.get(demand.ProjectedPublicLightingFacilityCount) + self.get(demand.ProjectedCommercialFacilityCount)


class GridInternalConnectionCount(V):
    
    section = 'system (grid)'
    option = 'internal connection count'
    aliases = ['GR_IntConnCt', 'gr_ic']

    short_section = 'GR'
    short_option = 'IntConnCt'

    dependencies = [
        demand.TargetHouseholdCount,
        GridSocialInfrastructureCount,
    ]
    units = 'connection count'
   
    def compute(self):
        return self.get(demand.TargetHouseholdCount) + self.get(GridSocialInfrastructureCount)


class GridTransformerDesiredSystemCapacity(V):

    section = 'system (grid)'
    option = 'grid transformer desired system capacity'
    aliases = ['GR_GRTfmrDsrdSysCpty', 'gr_tr_dcp']

    short_section = 'GR'
    short_option = 'GRTfmrDsrdSysCpty'

    dependencies = [
        demand.ProjectedPeakNodalDemand,
        DistributionLoss,
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(demand.ProjectedPeakNodalDemand) / float(1 - self.get(DistributionLoss))


class GridTransformerActualSystemCapacityCounts(V):

    section = 'system (grid)'
    option = 'grid transformer actual system capacity counts'
    aliases = ['GR_GRTfmrActlSysCptyCts', 'gr_tr_acps']

    short_section = 'GR'
    short_option = 'GRTfmrActlSysCptyCts'

    c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
    dependencies = [
        GridTransformerDesiredSystemCapacity,
        GridTransformerAvailableSystemCapacities,
    ]
    units = 'capacity count list'

    def compute(self):
        return metric.computeSystemCounts(
            self.get(GridTransformerDesiredSystemCapacity), 
            self.get(GridTransformerAvailableSystemCapacities))


class GridTransformerActualSystemCapacity(V):

    section = 'system (grid)'
    option = 'grid transformer actual system capacity'
    aliases = ['GR_GRTfmrActlSysCpty', 'gr_tr_acp']

    short_section = 'GR'
    short_option = 'GRTfmrActlSysCpty'

    dependencies = [
        GridTransformerAvailableSystemCapacities,
        GridTransformerActualSystemCapacityCounts,
    ]
    units = 'kilowatts'

    def compute(self):
        return numpy.dot(
            self.get(GridTransformerAvailableSystemCapacities), 
            self.get(GridTransformerActualSystemCapacityCounts))


class GridInstallationCost(V):

    section = 'system (grid)'
    option = 'installation cost'
    aliases = ['GR_InstCst', 'gr_i']

    short_section = 'GR'
    short_option = 'InstCst'

    dependencies = [
        GridInstallationCostPerConnection,
        GridInternalConnectionCount,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(GridInstallationCostPerConnection) * self.get(GridInternalConnectionCount) 


class LowVoltageLineEquipmentCost(V):

    section = 'system (grid)'
    option = 'low voltage line equipment cost'
    aliases = ['GR_LVLnEqmtCst', 'gr_le']

    short_section = 'GR'
    short_option = 'LVLnEqmtCst'

    dependencies = [
        costDistribution.LowVoltageLineEquipmentCostPerConnection,
        GridInternalConnectionCount,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(costDistribution.LowVoltageLineEquipmentCostPerConnection) * self.get(GridInternalConnectionCount)


class LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear(V):

    section = 'system (grid)'
    option = 'low voltage line equipment operations and maintenance cost per year'
    aliases = ['GR_LVLnEqmtOandMCstPrYr', 'gr_le_om']

    short_section = 'GR'
    short_option = 'LVLnEqmtOandMCstPrYr'

    dependencies = [
        costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost,
        LowVoltageLineEquipmentCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost) * self.get(LowVoltageLineEquipmentCost)


class GridTransformerCost(V):

    section = 'system (grid)'
    option = 'transformer cost'
    aliases = ['GR_TfmrCst', 'gr_tr']

    short_section = 'GR'
    short_option = 'TfmrCst'

    dependencies = [
        GridTransformerCostPerGridSystemKilowatt,
        GridTransformerActualSystemCapacity,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(GridTransformerCostPerGridSystemKilowatt) * self.get(GridTransformerActualSystemCapacity)


class GridTransformerOperationsAndMaintenanceCostPerYear(V):

    section = 'system (grid)'
    option = 'transformer operations and maintenance cost per year'
    aliases = ['GR_TfmrOandMCstPrYr', 'gr_tr_om']

    short_section = 'GR'
    short_option = 'TfmrOandMCstPrYr'

    dependencies = [
        GridTransformerOperationsAndMaintenanceCostPerYearAsFractionOfTransformerCost,
        GridTransformerCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(GridTransformerOperationsAndMaintenanceCostPerYearAsFractionOfTransformerCost) * self.get(GridTransformerCost)


class GridTransformerReplacementCostPerYear(V):

    section = 'system (grid)'
    option = 'transformer replacement cost per year'
    aliases = ['GR_TfmrRpmtCstPrYr', 'gr_tr_rep']

    short_section = 'GR'
    short_option = 'TfmrRpmtCstPrYr'

    dependencies = [
        GridTransformerCost,
        GridTransformerLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(GridTransformerCost) / float(self.get(GridTransformerLifetime))


class GridElectricityCostPerYear(V):

    section = 'system (grid)'
    option = 'electricity cost per year'
    aliases = ['GR_ElecCstPrYr', 'gr_el']

    short_section = 'GR'
    short_option = 'ElecCstPrYr'

    dependencies = [
        GridElectricityCostPerKilowattHour,
        demand.ProjectedNodalDemandPerYear,
        DistributionLoss,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(GridElectricityCostPerKilowattHour) * self.get(demand.ProjectedNodalDemandPerYear) / float(1 - self.get(DistributionLoss))


class GridInternalSystemInitialCost(V):

    section = 'system (grid)'
    option = 'internal system initial cost'
    aliases = ['GR_IntSysInitCst', 'gi_ini']

    short_section = 'GR'
    short_option = 'IntSysInitCst'

    dependencies = [
        GridInstallationCost,
        GridTransformerCost,
        LowVoltageLineEquipmentCost,
        costDistribution.LowVoltageLineInitialCost,
    ]
    units = 'dollars'

    def compute(self):
        return sum([
            self.get(GridInstallationCost),
            self.get(GridTransformerCost),
            self.get(LowVoltageLineEquipmentCost),
            self.get(costDistribution.LowVoltageLineInitialCost),
        ])


class GridInternalSystemRecurringCostPerYear(V):

    section = 'system (grid)'
    option = 'internal system recurring cost per year'
    aliases = ['GR_IntSysRcrgCstPrYr', 'gi_rec']

    short_section = 'GR'
    short_option = 'IntSysRcrgCstPrYr'

    dependencies = [
        GridTransformerOperationsAndMaintenanceCostPerYear,
        GridTransformerReplacementCostPerYear,
        GridElectricityCostPerYear,
        LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear,
        costDistribution.LowVoltageLineRecurringCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(GridTransformerOperationsAndMaintenanceCostPerYear),
            self.get(GridTransformerReplacementCostPerYear),
            self.get(GridElectricityCostPerYear),
            self.get(LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear),
            self.get(costDistribution.LowVoltageLineRecurringCostPerYear),
        ])


class GridInternalSystemNodalDiscountedCost(V):

    section = 'system (grid)'
    option = 'internal system nodal discounted cost'
    aliases = ['GR_IntSysNdlDsctdCst', 'gi_nod_d']

    short_section = 'GR'
    short_option = 'IntSysNdlDsctdCst'

    dependencies = [
        demand.ProjectedNodalDemandPerYear,
        GridInternalSystemInitialCost,
        GridInternalSystemRecurringCostPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'dollars'

    def compute(self):
        if self.get(demand.ProjectedNodalDemandPerYear) == 0:
            return 0
        return self.get(GridInternalSystemInitialCost) + self.get(GridInternalSystemRecurringCostPerYear) * self.get(finance.DiscountedCashFlowFactor)


class GridInternalSystemNodalLevelizedCost(V):

    section = 'system (grid)'
    option = 'internal system nodal levelized cost'
    aliases = ['GR_IntSysNdlLvlzdCst', 'gi_nod_lev']

    short_section = 'GR'
    short_option = 'IntSysNdlLvlzdCst'

    dependencies = [
        demand.ProjectedNodalDiscountedDemand,
        GridInternalSystemNodalDiscountedCost,
    ]
    units = 'dollars per kilowatt-hour'

    def compute(self):
        if self.get(demand.ProjectedNodalDiscountedDemand) == 0:
            return 0
        return self.get(GridInternalSystemNodalDiscountedCost) / float(self.get(demand.ProjectedNodalDiscountedDemand))


class GridMediumVoltageLineOperationsAndMaintenanceCostPerMeterPerYear(V):

    section = 'system (grid)'
    option = 'medium voltage line operations and maintenace cost per meter per year'
    aliases = ['GR_MVLnOandMCstPrMPrYr', 'gr_ml_omm']

    short_section = 'GR'
    short_option = 'MVLnOandMCstPrMPrYr'

    dependencies = [
        GridMediumVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost,
        GridMediumVoltageLineCostPerMeter,
    ]
    units = 'dollars per meter per year'

    def compute(self):
        return self.get(GridMediumVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost) * self.get(GridMediumVoltageLineCostPerMeter)


class GridMediumVoltageLineReplacementCostPerMeterPerYear(V):

    section = 'system (grid)'
    option = 'medium voltage line replacement cost per meter per year'
    aliases = ['GR_MVLnRpmtCstPrMPrYr', 'gr_ml_repm']

    short_section = 'GR'
    short_option = 'MVLnRpmtCstPrMPrYr'

    dependencies = [
        GridMediumVoltageLineCostPerMeter,
        GridMediumVoltageLineLifetime,
    ]
    units = 'dollars per meter per year'

    def compute(self):
        return self.get(GridMediumVoltageLineCostPerMeter) / float(self.get(GridMediumVoltageLineLifetime))


class GridExternalSystemInitialCostPerMeter(V):

    section = 'system (grid)'
    option = 'external system initial cost per meter'
    aliases = ['GR_ExtSysInitCstPrM', 'ge_inim']

    short_section = 'GR'
    short_option = 'ExtSysInitCstPrM'

    dependencies = [
        GridMediumVoltageLineCostPerMeter,
    ]
    units = 'dollars per meter'

    def compute(self):
        return self.get(GridMediumVoltageLineCostPerMeter)


class GridExternalSystemRecurringCostPerMeterPerYear(V):

    section = 'system (grid)'
    option = 'external system recurring cost per meter per year'
    aliases = ['GR_ExtSysRcrgCstPrMPrYr', 'ge_recm']

    short_section = 'GR'
    short_option = 'ExtSysRcrgCstPrMPrYr'

    dependencies = [
        GridMediumVoltageLineOperationsAndMaintenanceCostPerMeterPerYear,
        GridMediumVoltageLineReplacementCostPerMeterPerYear,
    ]
    units = 'dollars per meter per year'

    def compute(self):
        return self.get(GridMediumVoltageLineOperationsAndMaintenanceCostPerMeterPerYear) + self.get(GridMediumVoltageLineReplacementCostPerMeterPerYear)


class GridExternalSystemNodalDiscountedRecurringCostPerMeter(V):

    section = 'system (grid)'
    option = 'external nodal discounted recurring cost per meter'
    aliases = ['GR_ExtNdlDsctdRcrgCstPrM', 'ge_nodm_drcpm']

    short_section = 'GR'
    short_option = 'ExtNdlDsctdRcrgCstPrM'

    c = dict(check=store.assertPositive)
    dependencies = [
        GridExternalSystemRecurringCostPerMeterPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'dollars per meter'

    def compute(self):
        return self.get(GridExternalSystemRecurringCostPerMeterPerYear) * self.get(finance.DiscountedCashFlowFactor)


class GridExternalSystemNodalDiscountedCostPerMeter(V):

    section = 'system (grid)'
    option = 'external nodal discounted cost per meter'
    aliases = ['GR_ExtNdlDsctdCstPrM', 'ge_nodm_d']

    short_section = 'GR'
    short_option = 'ExtNdlDsctdCstPrM'

    c = dict(check=store.assertPositive)
    dependencies = [
        GridExternalSystemInitialCostPerMeter,
        GridExternalSystemNodalDiscountedRecurringCostPerMeter,
    ]
    units = 'dollars per meter'

    def compute(self):
        return self.get(GridExternalSystemInitialCostPerMeter) + self.get(GridExternalSystemNodalDiscountedRecurringCostPerMeter)


