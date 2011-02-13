'Estimate the construction and maintenance cost of an off-grid system'
# Import system modules
import numpy
# Import custom modules
from np.lib.variable_store import Variable as V
from np.lib import store, metric
import finance
import demographics
import demand
import costMiniGrid



# Off-grid system cost parameters


class PhotovoltaicPanelAvailableSystemCapacities(V):

    section = 'system (off-grid)'
    option = 'available system capacities (photovoltaic panel)'
    aliases = ['og_pp_cps']
    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1.5 1.0 0.4 0.15 0.075 0.05'
    units = 'kilowatts list'


class PhotovoltaicPanelCostPerPhotovoltaicComponentKilowatt(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel cost per photovoltaic component kilowatt'
    aliases = ['og_pp_ckw']
    default = 6000
    units = 'dollars per kilowatt'


class PhotovoltaicBalanceCostAsFractionOfPanelCost(V):

    section = 'system (off-grid)'
    option = 'photovoltaic balance cost as fraction of panel cost'
    aliases = ['og_px_cf']
    default = 0.5


class PhotovoltaicBatteryKilowattHoursPerPhotovoltaicComponentKilowatt(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery kilowatt-hours per photovoltaic component kilowatt'
    aliases = ['og_pb_hkw']
    default = 5
    units = 'kilowatt-hours per kilowatt'


class PhotovoltaicBatteryCostPerKilowattHour(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery cost per kilowatt-hour'
    aliases = ['og_pb_ckwh']
    default = 400
    units = 'dollars per kilowatt-hour'


class PhotovoltaicPanelLifetime(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel lifetime'
    aliases = ['og_pp_life']
    c = dict(check=store.assertPositive)
    default = 30
    units = 'years'


class PhotovoltaicBalanceLifetime(V):

    section = 'system (off-grid)'
    option = 'photovoltaic balance lifetime'
    aliases = ['og_px_life']
    c = dict(check=store.assertPositive)
    default = 10
    units = 'years'


class PhotovoltaicBatteryLifetime(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery lifetime'
    aliases = ['og_pb_life']
    c = dict(check=store.assertPositive)
    default = 3
    units = 'years'


class PhotovoltaicComponentOperationsAndMaintenanceCostPerYearAsFractionOfComponentCost(V):

    section = 'system (off-grid)'
    option = 'photovoltaic component operations and maintenance cost per year as fraction of component cost'
    aliases = ['og_p_omf']
    default = 0.05


class DieselGeneratorAvailableSystemCapacities(costMiniGrid.DieselGeneratorAvailableSystemCapacities):

    section = 'system (off-grid)'
    default = '1000 750 500 400 200 150 100 70 32 19 12 10 8 6'
    aliases = ['og_dg_cps']


class DieselGeneratorHoursOfOperationPerYear(costMiniGrid.DieselGeneratorHoursOfOperationPerYear):

    section = 'system (off-grid)'
    default = 2500
    aliases = ['og_dg_hr']



# Photovoltaic intermediates


class PhotovoltaicPanelDesiredSystemCapacity(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel desired capacity'
    aliases = ['og_pp_dcp']
    dependencies = [
        demand.ProjectedPeakHouseholdDemand,
        demand.ProjectedPeakHealthFacilityDemand,
        demand.ProjectedPeakEducationFacilityDemand,
        demand.ProjectedPeakPublicLightingFacilityDemand,
    ]
    units = 'kilowatts'

    def compute(self):
        return sum([
            self.get(demand.ProjectedPeakHouseholdDemand),
            self.get(demand.ProjectedPeakHealthFacilityDemand),
            self.get(demand.ProjectedPeakEducationFacilityDemand),
            self.get(demand.ProjectedPeakPublicLightingFacilityDemand),
        ])


class PhotovoltaicPanelActualSystemCapacityCounts(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel actual capacity counts'
    aliases = ['og_pp_acps']
    c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
    dependencies = [
        PhotovoltaicPanelDesiredSystemCapacity,
        PhotovoltaicPanelAvailableSystemCapacities,
    ]
    units = 'capacity count list'

    def compute(self):
        return metric.computeSystemCounts(
            self.get(PhotovoltaicPanelDesiredSystemCapacity), 
            self.get(PhotovoltaicPanelAvailableSystemCapacities))


class PhotovoltaicPanelActualSystemCapacity(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel actual capacity'
    aliases = ['og_pp_acp']
    dependencies = [
        PhotovoltaicPanelAvailableSystemCapacities,
        PhotovoltaicPanelActualSystemCapacityCounts,
    ]
    units = 'kilowatts'

    def compute(self):
        return numpy.dot(
            self.get(PhotovoltaicPanelAvailableSystemCapacities), 
            self.get(PhotovoltaicPanelActualSystemCapacityCounts))


class PhotovoltaicPanelCost(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel cost'
    aliases = ['og_pp_ini']
    dependencies = [
        PhotovoltaicPanelCostPerPhotovoltaicComponentKilowatt,
        PhotovoltaicPanelActualSystemCapacity,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(PhotovoltaicPanelCostPerPhotovoltaicComponentKilowatt) * self.get(PhotovoltaicPanelActualSystemCapacity)


class PhotovoltaicPanelReplacementCostPerYear(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel replacement cost per year'
    aliases = ['og_pp_rep']
    dependencies = [
        PhotovoltaicPanelCost,
        PhotovoltaicPanelLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(PhotovoltaicPanelCost) / float(self.get(PhotovoltaicPanelLifetime))


class PhotovoltaicBatteryCost(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery cost'
    aliases = ['og_pb_ini']
    dependencies = [
        PhotovoltaicBatteryCostPerKilowattHour,
        PhotovoltaicBatteryKilowattHoursPerPhotovoltaicComponentKilowatt,
        PhotovoltaicPanelActualSystemCapacity,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(PhotovoltaicBatteryCostPerKilowattHour) * self.get(PhotovoltaicBatteryKilowattHoursPerPhotovoltaicComponentKilowatt) * self.get(PhotovoltaicPanelActualSystemCapacity)


class PhotovoltaicBatteryReplacementCostPerYear(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery replacement cost per year'
    aliases = ['og_pb_rep']
    dependencies = [
        PhotovoltaicBatteryCost,
        PhotovoltaicBatteryLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(PhotovoltaicBatteryCost) / float(self.get(PhotovoltaicBatteryLifetime))


class PhotovoltaicBalanceCost(V):
    """
    The balance consists of the parts of the photovoltaic system besides 
    the panels and the batteries.
    """

    section = 'system (off-grid)'
    option = 'photovoltaic balance cost'
    aliases = ['og_px_ini']
    dependencies = [
        PhotovoltaicBalanceCostAsFractionOfPanelCost,
        PhotovoltaicPanelCost,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(PhotovoltaicBalanceCostAsFractionOfPanelCost) * self.get(PhotovoltaicPanelCost)


class PhotovoltaicBalanceReplacementCostPerYear(V):

    section = 'system (off-grid)'
    option = 'photovoltaic balance replacement cost per year'
    aliases = ['og_px_rep']
    dependencies = [
        PhotovoltaicBalanceCost,
        PhotovoltaicBalanceLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(PhotovoltaicBalanceCost) / float(self.get(PhotovoltaicBalanceLifetime))


class PhotovoltaicComponentInitialCost(V):

    section = 'system (off-grid)'
    option = 'photovoltaic component initial cost'
    aliases = ['og_p_ini']
    dependencies = [
        PhotovoltaicPanelCost,
        PhotovoltaicBatteryCost,
        PhotovoltaicBalanceCost,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(PhotovoltaicPanelCost) + self.get(PhotovoltaicBatteryCost) + self.get(PhotovoltaicBalanceCost)


class PhotovoltaicComponentOperationsAndMaintenanceCostPerYear(V):

    section = 'system (off-grid)'
    option = 'photovoltaic component operations and maintenance cost per year'
    aliases = ['og_p_om']
    dependencies = [
        PhotovoltaicComponentOperationsAndMaintenanceCostPerYearAsFractionOfComponentCost,
        PhotovoltaicComponentInitialCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(PhotovoltaicComponentOperationsAndMaintenanceCostPerYearAsFractionOfComponentCost) * self.get(PhotovoltaicComponentInitialCost)


class PhotovoltaicComponentRecurringCostPerYear(V):

    section = 'system (off-grid)'
    option = 'photovoltaic component recurring cost per year'
    aliases = ['og_p_rec']
    dependencies = [
        PhotovoltaicPanelReplacementCostPerYear,
        PhotovoltaicBatteryReplacementCostPerYear,
        PhotovoltaicBalanceReplacementCostPerYear,
        PhotovoltaicComponentOperationsAndMaintenanceCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(PhotovoltaicPanelReplacementCostPerYear) + self.get(PhotovoltaicBatteryReplacementCostPerYear) + self.get(PhotovoltaicBalanceReplacementCostPerYear) + self.get(PhotovoltaicComponentOperationsAndMaintenanceCostPerYear)



# Diesel intermediates


class DieselGeneratorDesiredSystemCapacity(costMiniGrid.DieselGeneratorDesiredSystemCapacity):

    section = 'system (off-grid)'
    aliases = ['og_dg_dcp']
    dependencies = [
        demand.ProjectedPeakCommercialFacilityDemand,
        demand.ProjectedPeakProductiveDemand,
    ]

    def compute(self):
        return sum([
            self.get(demand.ProjectedPeakCommercialFacilityDemand),
            self.get(demand.ProjectedPeakProductiveDemand),
        ])


class DieselGeneratorActualSystemCapacityCounts(costMiniGrid.DieselGeneratorActualSystemCapacityCounts):

    section = 'system (off-grid)'
    aliases = ['og_dg_acps']
    dependencies = [
        DieselGeneratorDesiredSystemCapacity,
        DieselGeneratorAvailableSystemCapacities,
    ]

    def compute(self):
        return metric.computeSystemCounts(
            self.get(DieselGeneratorDesiredSystemCapacity), 
            self.get(DieselGeneratorAvailableSystemCapacities))


class DieselGeneratorActualSystemCapacity(costMiniGrid.DieselGeneratorActualSystemCapacity):

    section = 'system (off-grid)'
    aliases = ['og_dg_acp']
    dependencies = [
        DieselGeneratorAvailableSystemCapacities,
        DieselGeneratorActualSystemCapacityCounts,
    ]

    def compute(self):
        return numpy.dot(
            self.get(DieselGeneratorAvailableSystemCapacities), 
            self.get(DieselGeneratorActualSystemCapacityCounts))


class DieselEquipmentCost(V):

    section = 'system (off-grid)'
    option = 'diesel equipment cost'
    aliases = ['og_de_ini']
    dependencies = [
        costMiniGrid.DieselEquipmentCostPerConnection,
        demand.ProjectedCommercialFacilityCount,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(costMiniGrid.DieselEquipmentCostPerConnection) * self.get(demand.ProjectedCommercialFacilityCount)


class DieselEquipmentOperationsAndMaintenanceCostPerYear(costMiniGrid.DieselEquipmentOperationsAndMaintenanceCostPerYear):

    section = 'system (off-grid)'
    aliases = ['og_de_om']
    dependencies = [
        costMiniGrid.DieselEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost,
        DieselEquipmentCost,
    ]
    
    def compute(self):
        return self.get(costMiniGrid.DieselEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost) * self.get(DieselEquipmentCost)


class DieselGeneratorCost(costMiniGrid.DieselGeneratorCost):

    section = 'system (off-grid)'
    aliases = ['og_dg_ini']
    dependencies = [
        costMiniGrid.DieselGeneratorCostPerDieselSystemKilowatt,
        DieselGeneratorActualSystemCapacity,
    ]

    def compute(self):
        return self.get(costMiniGrid.DieselGeneratorCostPerDieselSystemKilowatt) * self.get(DieselGeneratorActualSystemCapacity)


class DieselGeneratorInstallationCost(costMiniGrid.DieselGeneratorInstallationCost):

    section = 'system (off-grid)'
    aliases = ['og_dg_i']
    dependencies = [
        costMiniGrid.DieselGeneratorInstallationCostAsFractionOfGeneratorCost,
        DieselGeneratorCost,
    ]

    def compute(self):
        return self.get(costMiniGrid.DieselGeneratorInstallationCostAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)


class DieselGeneratorOperationsAndMaintenanceCostPerYear(costMiniGrid.DieselGeneratorOperationsAndMaintenanceCostPerYear):

    section = 'system (off-grid)'
    aliases = ['og_dg_om']
    dependencies = [
        costMiniGrid.DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost,
        DieselGeneratorCost,
    ]

    def compute(self):
        return self.get(costMiniGrid.DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)


class DieselGeneratorReplacementCostPerYear(costMiniGrid.DieselGeneratorReplacementCostPerYear):

    section = 'system (off-grid)'
    aliases = ['og_dg_rep']
    dependencies = [
        DieselGeneratorCost,
        costMiniGrid.DieselGeneratorLifetime,
    ]

    def compute(self):
        return self.get(DieselGeneratorCost) / float(self.get(costMiniGrid.DieselGeneratorLifetime))


class DieselFuelCostPerYear(costMiniGrid.DieselFuelCostPerYear):

    section = 'system (off-grid)'
    aliases = ['og_fl']
    dependencies = [
        costMiniGrid.DieselFuelCostPerLiter,
        costMiniGrid.DieselFuelLitersConsumedPerKilowattHour,
        DieselGeneratorActualSystemCapacity,
        DieselGeneratorHoursOfOperationPerYear,
    ]

    def compute(self):
        return self.get(costMiniGrid.DieselFuelCostPerLiter) * self.get(costMiniGrid.DieselFuelLitersConsumedPerKilowattHour) * self.get(DieselGeneratorActualSystemCapacity) * self.get(DieselGeneratorHoursOfOperationPerYear)


class DieselComponentInitialCost(costMiniGrid.MiniGridSystemInitialCost):

    section = 'system (off-grid)'
    option = 'diesel component initial cost'
    aliases = ['og_d_ini']
    dependencies = [
        DieselGeneratorCost,
        DieselGeneratorInstallationCost,
        DieselEquipmentCost,
    ]

    def compute(self):
        return sum([
            self.get(DieselGeneratorCost),
            self.get(DieselGeneratorInstallationCost),
            self.get(DieselEquipmentCost),
        ])


class DieselComponentRecurringCostPerYear(costMiniGrid.MiniGridSystemRecurringCostPerYear):

    section = 'system (off-grid)'
    option = 'diesel component recurring cost per year'
    aliases = ['og_d_rec']
    dependencies = [
        DieselGeneratorOperationsAndMaintenanceCostPerYear,
        DieselEquipmentOperationsAndMaintenanceCostPerYear,
        DieselGeneratorReplacementCostPerYear,
        DieselFuelCostPerYear,
    ]

    def compute(self):
        return sum([
            self.get(DieselGeneratorOperationsAndMaintenanceCostPerYear),
            self.get(DieselEquipmentOperationsAndMaintenanceCostPerYear),
            self.get(DieselGeneratorReplacementCostPerYear),
            self.get(DieselFuelCostPerYear),
        ])



# System costs


class OffGridSystemInitialCost(V):

    section = 'system (off-grid)'
    option = 'system initial cost'
    aliases = ['og_ini']
    dependencies = [
        PhotovoltaicComponentInitialCost,
        DieselComponentInitialCost,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(PhotovoltaicComponentInitialCost) + self.get(DieselComponentInitialCost)


class OffGridSystemRecurringCostPerYear(V):

    section = 'system (off-grid)'
    option = 'system recurring cost per year'
    aliases = ['og_rec']
    dependencies = [
        PhotovoltaicComponentRecurringCostPerYear,
        DieselComponentRecurringCostPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return self.get(PhotovoltaicComponentRecurringCostPerYear) + self.get(DieselComponentRecurringCostPerYear)


class OffGridSystemNodalDiscountedCost(V):

    section = 'system (off-grid)'
    option = 'system nodal discounted cost'
    aliases = ['og_nod_d']
    dependencies = [
        demand.ProjectedNodalDemandPerYear,
        OffGridSystemInitialCost,
        OffGridSystemRecurringCostPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'dollars'

    def compute(self):
        if self.get(demand.ProjectedNodalDemandPerYear) == 0:
            return 0
        return self.get(OffGridSystemInitialCost) + self.get(OffGridSystemRecurringCostPerYear) * self.get(finance.DiscountedCashFlowFactor)


class OffGridSystemNodalLevelizedCost(V):

    section = 'system (off-grid)'
    option = 'system nodal levelized cost'
    aliases = ['og_nod_lev']
    dependencies = [
        demand.ProjectedNodalDiscountedDemand,
        OffGridSystemNodalDiscountedCost,
    ]
    units = 'dollars per kilowatt-hour'

    def compute(self):
        if self.get(demand.ProjectedNodalDiscountedDemand) == 0:
            return 0
        return self.get(OffGridSystemNodalDiscountedCost) / float(self.get(demand.ProjectedNodalDiscountedDemand))
