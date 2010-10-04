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
    aliases = ['gr_loss']
    c = dict(check=store.assertLessThanOne)
    default = 0.15
    units = 'fraction'


class GridElectricityCostPerKilowattHour(V):

    section = 'system (grid)'
    option = 'electricity cost per kilowatt-hour'
    aliases = ['gr_el_ckwh']
    default = 0.17
    units = 'dollars per kilowatt-hour'


class GridTransformerAvailableSystemCapacities(V):

    section = 'system (grid)'
    option = 'available system capacities (transformer)'
    aliases = ['gr_tr_cps']
    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1000 900 800 700 600 500 400 300 200 100 90 80 70 60 50 40 30 20 15 5'
    units = 'kilowatts list'


class GridTransformerCostPerGridSystemKilowatt(V):

    section = 'system (grid)'
    option = 'transformer cost per grid system kilowatt'
    aliases = ['gr_tr_ckw']
    default = 1000
    units = 'dollars per kilowatt'

    
class GridTransformerLifetime(V):

    section = 'system (grid)'
    option = 'transformer lifetime'
    aliases = ['gr_tr_life']
    c = dict(check=store.assertPositive)
    default = 10
    units = 'years'


class GridTransformerOperationsAndMaintenanceCostPerYearAsFractionOfTransformerCost(V):

    section = 'system (grid)'
    option = 'transformer operations and maintenance cost per year as fraction of transformer cost'
    aliases = ['gr_tr_omf']
    default = 0.03


class GridEquipmentCostPerConnection(V):

    section = 'system (grid)'
    option = 'equipment cost per connection'
    aliases = ['gr_e_cc']
    default = 200
    units = 'dollars per connection'


class GridInstallationCostPerConnection(V):

    section = 'system (grid)'
    option = 'installation cost per connection'
    aliases = ['gr_i_cc']
    default = 60
    units = 'dollars per connection'


class GridServiceCostPerConnection(V):

    section = 'system (grid)'
    option = 'service cost per connection'
    aliases = ['gr_s_cc']
    default = 70
    units = 'dollars per connection'


class GridEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost(V):

    section = 'system (grid)'
    option = 'equipment operations and maintenance cost per year as fraction of equipment cost'
    aliases = ['gr_e_omf']
    default = 0.01


class GridServiceOperationsAndMaintenanceCostPerYearAsFractionOfServiceCost(V):

    section = 'system (grid)'
    option = 'service operations and maintenance cost per year as fraction of service cost'
    aliases = ['gr_s_omf']
    default = 0.01


class GridMediumVoltageLineCostPerMeter(V):

    section = 'system (grid)'
    option = 'medium voltage line cost per meter'
    aliases = ['gr_ml_cm']
    default = 20
    units = 'dollars per meter'


class GridMediumVoltageLineLifetime(V):

    section = 'system (grid)'
    option = 'medium voltage line lifetime'
    aliases = ['gr_ml_life']
    c = dict(check=store.assertPositive)
    default = 30
    units = 'years'


class GridMediumVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost(V):

    section = 'system (grid)'
    option = 'medium voltage line operations and maintenance cost per year as fraction of line cost'
    aliases = ['gr_ml_omf']
    default = 0.01



# Grid system cost derivatives


class GridSocialInfrastructureCount(V):
    
    section = 'system (grid)'
    option = 'social infrastructure count'
    aliases = ['gr_so']
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
    aliases = ['gr_ic']
    dependencies = [
        demographics.ProjectedHouseholdCount,
        GridSocialInfrastructureCount,
    ]
    units = 'connection count'
   
    def compute(self):
        return self.get(demographics.ProjectedHouseholdCount) + self.get(GridSocialInfrastructureCount)


class GridTransformerDesiredSystemCapacity(V):

    section = 'system (grid)'
    option = 'grid transformer desired system capacity'
    aliases = ['gr_tr_dcp']
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
    aliases = ['gr_tr_acps']
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
    aliases = ['gr_tr_acp']
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
    aliases = ['gr_i']
    dependencies = [
        GridInstallationCostPerConnection,
        GridInternalConnectionCount,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(GridInstallationCostPerConnection) * self.get(GridInternalConnectionCount) 


class GridServiceCost(V):

    section = 'system (grid)'
    option = 'service cost'
    aliases = ['gr_s']
    dependencies = [
        GridServiceCostPerConnection,
        GridInternalConnectionCount,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(GridServiceCostPerConnection) * self.get(GridInternalConnectionCount)


class GridServiceOperationsAndMaintenanceCostPerYear(V):

    section = 'system (grid)'
    option = 'service operations and maintenance cost per year'
    aliases = ['gr_s_om']
    dependencies = [
        GridServiceOperationsAndMaintenanceCostPerYearAsFractionOfServiceCost,
        GridServiceCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(GridServiceOperationsAndMaintenanceCostPerYearAsFractionOfServiceCost) * self.get(GridServiceCost)


class GridEquipmentCost(V):

    section = 'system (grid)'
    option = 'equipment cost'
    aliases = ['gr_e']
    dependencies = [
        GridEquipmentCostPerConnection,
        GridInternalConnectionCount,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(GridEquipmentCostPerConnection) * self.get(GridInternalConnectionCount)


class GridEquipmentOperationsAndMaintenanceCostPerYear(V):

    section = 'system (grid)'
    option = 'equipment operations and maintenance cost per year'
    aliases = ['gr_e_om']
    dependencies = [
        GridEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost,
        GridEquipmentCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(GridEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost) * self.get(GridEquipmentCost)


class GridTransformerCost(V):

    section = 'system (grid)'
    option = 'transformer cost'
    aliases = ['gr_tr']
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
    aliases = ['gr_tr_om']
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
    aliases = ['gr_tr_rep']
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
    aliases = ['gr_el']
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
    aliases = ['gi_ini']
    dependencies = [
        GridInstallationCost,
        GridTransformerCost,
        GridEquipmentCost,
        GridServiceCost,
        costDistribution.LowVoltageLineInitialCost,
    ]
    units = 'dollars'

    def compute(self):
        return sum([
            self.get(GridInstallationCost),
            self.get(GridTransformerCost),
            self.get(GridEquipmentCost),
            self.get(GridServiceCost),
            self.get(costDistribution.LowVoltageLineInitialCost),
        ])


class GridInternalSystemRecurringCostPerYear(V):

    section = 'system (grid)'
    option = 'internal system recurring cost per year'
    aliases = ['gi_rec']
    dependencies = [
        GridTransformerOperationsAndMaintenanceCostPerYear,
        GridEquipmentOperationsAndMaintenanceCostPerYear,
        GridServiceOperationsAndMaintenanceCostPerYear,
        GridTransformerReplacementCostPerYear,
        GridElectricityCostPerYear,
        costDistribution.LowVoltageLineRecurringCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return sum([
            self.get(GridTransformerOperationsAndMaintenanceCostPerYear),
            self.get(GridEquipmentOperationsAndMaintenanceCostPerYear),
            self.get(GridServiceOperationsAndMaintenanceCostPerYear),
            self.get(GridTransformerReplacementCostPerYear),
            self.get(GridElectricityCostPerYear),
            self.get(costDistribution.LowVoltageLineRecurringCostPerYear),
        ])


class GridInternalSystemNodalDiscountedCost(V):

    section = 'system (grid)'
    option = 'internal system nodal discounted cost'
    aliases = ['gi_nod_d']
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
    aliases = ['gi_nod_lev']
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
    aliases = ['gr_ml_omm']
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
    aliases = ['gr_ml_repm']
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
    aliases = ['ge_inim']
    dependencies = [
        GridMediumVoltageLineCostPerMeter,
    ]
    units = 'dollars per meter'

    def compute(self):
        return self.get(GridMediumVoltageLineCostPerMeter)


class GridExternalSystemRecurringCostPerMeterPerYear(V):

    section = 'system (grid)'
    option = 'external system recurring cost per meter per year'
    aliases = ['ge_recm']
    dependencies = [
        GridMediumVoltageLineOperationsAndMaintenanceCostPerMeterPerYear,
        GridMediumVoltageLineReplacementCostPerMeterPerYear,
    ]
    units = 'dollars per meter per year'

    def compute(self):
        return self.get(GridMediumVoltageLineOperationsAndMaintenanceCostPerMeterPerYear) + self.get(GridMediumVoltageLineReplacementCostPerMeterPerYear)


class GridExternalSystemNodalDiscountedCostPerMeter(V):

    section = 'system (grid)'
    option = 'external nodal discounted cost per meter'
    aliases = ['ge_nodm_d']
    c = dict(check=store.assertPositive)
    dependencies = [
        GridExternalSystemInitialCostPerMeter,
        GridExternalSystemRecurringCostPerMeterPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'dollars per meter'

    def compute(self):
        return self.get(GridExternalSystemInitialCostPerMeter) + self.get(GridExternalSystemRecurringCostPerMeterPerYear) * self.get(finance.DiscountedCashFlowFactor)
