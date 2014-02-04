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


class PeakSunHoursPerYear(V):
    """
    Peak sun hours is the number of hours per year during which sunlight
    is considered brightest for a given location.
    """

    section = 'system (off-grid)'
    option = 'peak sun hours per year'
    aliases = ['og_pk_sun_hrs_pr_yr', 'pksu_hr']


    c = dict(check=store.assertPositive)
    default = 1320
    units = 'hours per year'


class PhotovoltaicPanelAvailableSystemCapacities(V):

    section = 'system (off-grid)'
    option = 'available system capacities (photovoltaic panel)'
    aliases = ['og_avbl_sys_cap_pv_pnl', 'og_pp_cps']


    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1.5 1.0 0.4 0.15 0.075 0.05'
    units = 'kilowatts list'


class PhotovoltaicPanelCostPerPhotovoltaicComponentKilowatt(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel cost per photovoltaic component kilowatt'
    aliases = ['og_pv_pnl_cst_pr_pv_cmpt_kw', 'og_pp_ckw']


    default = 6000
    units = 'dollars per kilowatt'


class PhotovoltaicBalanceCostAsFractionOfPanelCost(V):

    section = 'system (off-grid)'
    option = 'photovoltaic balance cost as fraction of panel cost'
    aliases = ['og_pv_bal_cst_as_fctn_of_pnl_cst', 'og_px_cf']


    default = 0.5


class PhotovoltaicBatteryKilowattHoursPerPhotovoltaicComponentKilowatt(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery kilowatt-hours per photovoltaic component kilowatt'
    aliases = ['og_pv_batt_kw_hr_pr_pv_cmpt_kw', 'og_pb_hkw']


    default = 5
    units = 'kilowatt-hours per kilowatt'


class PhotovoltaicBatteryCostPerKilowattHour(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery cost per kilowatt-hour'
    aliases = ['og_pv_batt_cst_pr_kw_hr', 'og_pb_ckwh']


    default = 400
    units = 'dollars per kilowatt-hour'


class PhotovoltaicPanelLifetime(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel lifetime'
    aliases = ['og_pv_pnl_life', 'og_pp_life']


    c = dict(check=store.assertPositive)
    default = 30
    units = 'years'


class PhotovoltaicBalanceLifetime(V):

    section = 'system (off-grid)'
    option = 'photovoltaic balance lifetime'
    aliases = ['og_pv_bal_life', 'og_px_life']


    c = dict(check=store.assertPositive)
    default = 10
    units = 'years'


class PhotovoltaicBatteryLifetime(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery lifetime'
    aliases = ['og_pv_batt_life', 'og_pb_life']


    c = dict(check=store.assertPositive)
    default = 3
    units = 'years'


class PhotovoltaicComponentEfficiencyLoss(V):

    section = 'system (off-grid)'
    option = 'photovoltaic component efficiency loss'
    aliases = ['og_pv_cmpt_efcy_lss', 'og_p_loss']


    c = dict(check=store.assertLessThanOne)
    default = 0.1
    units = 'fraction'


class PhotovoltaicComponentOperationsAndMaintenanceCostPerYearAsFractionOfComponentCost(V):

    section = 'system (off-grid)'
    option = 'photovoltaic component operations and maintenance cost per year as fraction of component cost'
    aliases = ['og_pv_cmpt_o_and_m_cst_pr_yr_as_fctn_of_cmpt_cst', 'og_p_omf']


    default = 0.05


class DieselGeneratorAvailableSystemCapacities(V):

    section = 'system (off-grid)'
    option = 'available system capacities (diesel generator)'
    aliases = ['og_avbl_sys_cap_dsl_gntr', 'og_dg_cps']


    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1000 750 500 400 200 150 100 70 32 19 12 10 8 6'
    units = 'kilowatts list'


class DieselGeneratorCostPerDieselSystemKilowatt(V):

    section = 'system (off-grid)'
    option = 'diesel generator cost per diesel system kilowatt'
    aliases = ['og_dsl_gntr_cst_pr_dsl_sys_kw', 'og_dg_ck']


    default = 150
    units = 'dollars per kilowatt'

class DieselGeneratorInstallationCostAsFractionOfGeneratorCost(V):

    section = 'system (off-grid)'
    aliases = ['og_dsl_gntr_inst_cst_as_fctn_of_gntr_cst', 'og_dg_if']


    option = 'diesel generator installation cost as fraction of generator cost'
    default = 0.25


class DieselGeneratorLifetime(V):

    section = 'system (off-grid)'
    option = 'diesel generator lifetime'
    aliases = ['og_dsl_gntr_life', 'og_dg_life']


    c = dict(check=store.assertPositive)
    default = 5
    units = 'years'


class DieselFuelCostPerLiter(V):

    section = 'system (off-grid)'
    option = 'diesel fuel cost per liter'
    aliases = ['og_dsl_cst_pr_ltr', 'og_fl_cl']


    default = 1.08
    units = 'dollars per liter'


class DieselFuelLitersConsumedPerKilowattHour(V):

    section = 'system (off-grid)'
    option = 'diesel fuel liters consumed per kilowatt-hour'
    aliases = ['og_dsl_ltr_csmd_pr_kw_hr', 'og_fl_lkwh']


    default = 0.5
    units = 'liters per kilowatt-hour'


class DieselGeneratorMinimumHoursOfOperationPerYear(V):

    section = 'system (off-grid)'
    option = 'diesel generator hours of operation per year (minimum)'
    aliases = ['og_dsl_gntr_hrs_of_oprn_pr_yr_min', 'og_dg_mnhr']


    default = 1460
    units = 'hours per year'


class DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost(V):

    section = 'system (off-grid)'
    option = 'diesel generator operations and maintenance cost per year as fraction of generator cost'
    aliases = ['og_dsl_gntr_o_and_m_cst_pr_yr_as_fctn_of_gntr_cst', 'og_dg_omf']


    default = 0.01


# Photovoltaic intermediates


class PhotovoltaicPanelDesiredSystemCapacity(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel desired capacity'
    aliases = ['og_pv_pnl_dsrd_cpty', 'og_pp_dcp']


    dependencies = [
        demand.ProjectedHouseholdDemandPerYear,
        demand.ProjectedHealthFacilityDemandPerYear,
        demand.ProjectedEducationFacilityDemandPerYear,
        demand.ProjectedPublicLightingFacilityDemandPerYear,
        PhotovoltaicComponentEfficiencyLoss,
        PeakSunHoursPerYear,
    ]
    units = 'kilowatts'

    def compute(self):
        # Computed effectiveDemandPerYear scaled by photovoltaic component loss
        effectiveDemandPerYear = sum([
            self.get(demand.ProjectedHouseholdDemandPerYear),
            self.get(demand.ProjectedHealthFacilityDemandPerYear),
            self.get(demand.ProjectedEducationFacilityDemandPerYear),
            self.get(demand.ProjectedPublicLightingFacilityDemandPerYear),
        ]) / float(1 - self.get(PhotovoltaicComponentEfficiencyLoss))
        # Return
        return effectiveDemandPerYear / float(self.get(PeakSunHoursPerYear))


class PhotovoltaicPanelActualSystemCapacityCounts(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel actual capacity counts'
    aliases = ['og_pv_pnl_actl_cpty_cts', 'og_pp_acps']


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
    aliases = ['og_pv_pnl_actl_cpty', 'og_pp_acp']


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
    aliases = ['og_pv_pnl_cst', 'og_pp_ini']


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
    aliases = ['og_pv_pnl_rpmt_cst_pr_yr', 'og_pp_rep']


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
    aliases = ['og_pv_batt_cst', 'og_pb_ini']


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
    aliases = ['og_pv_batt_rpmt_cst_pr_yr', 'og_pb_rep']


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
    aliases = ['og_pv_bal_cst', 'og_px_ini']


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
    aliases = ['og_pv_bal_rpmt_cst_pr_yr', 'og_px_rep']


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
    aliases = ['og_pv_cmpt_init_cst', 'og_p_ini']


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
    aliases = ['og_pv_cmpt_o_and_m_cst_pr_yr', 'og_p_om']


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
    aliases = ['og_pv_cmpt_rcrg_cst_pr_yr', 'og_p_rec']


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


class DieselGeneratorDesiredSystemCapacity(V):

    section = 'system (off-grid)'
    option = 'diesel generator desired system capacity'
    aliases = ['og_dsl_gntr_dsrd_sys_cpty', 'og_dg_dcp']


    dependencies = [
        demand.ProjectedPeakCommercialFacilityDemand,
        demand.ProjectedPeakProductiveDemand,
    ]
    units = 'kilowatts'

    def compute(self):
        return sum([
            self.get(demand.ProjectedPeakCommercialFacilityDemand),
            self.get(demand.ProjectedPeakProductiveDemand),
        ])


class DieselGeneratorActualSystemCapacityCounts(V):

    section = 'system (off-grid)'
    option = 'diesel generator actual system capacity counts'
    aliases = ['og_dsl_gntr_actl_sys_cpty_cts', 'og_dg_acps']


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

    section = 'system (off-grid)'
    option = 'diesel generator actual system capacity'
    aliases = ['og_dsl_gntr_actl_sys_cpty', 'og_dg_acp']


    dependencies = [
        DieselGeneratorAvailableSystemCapacities,
        DieselGeneratorActualSystemCapacityCounts,
    ]
    units = 'kilowatts'

    def compute(self):
        return numpy.dot(
            self.get(DieselGeneratorAvailableSystemCapacities), 
            self.get(DieselGeneratorActualSystemCapacityCounts))


class DieselGeneratorCost(V):

    section = 'system (off-grid)'
    option = 'diesel generator cost'
    aliases = ['og_dsl_gntr_cst', 'og_dg_ini']


    dependencies = [
        DieselGeneratorCostPerDieselSystemKilowatt,
        DieselGeneratorActualSystemCapacity,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(DieselGeneratorCostPerDieselSystemKilowatt) * 
                self.get(DieselGeneratorActualSystemCapacity))


class DieselGeneratorInstallationCost(V):

    section = 'system (off-grid)'
    option = 'diesel generator installation cost'
    aliases = ['og_dsl_gntr_inst_cst', 'og_dg_i']


    dependencies = [
        DieselGeneratorInstallationCostAsFractionOfGeneratorCost,
        DieselGeneratorCost,
    ]
    units = 'dollars'

    def compute(self):
        return (self.get(DieselGeneratorInstallationCostAsFractionOfGeneratorCost) * 
                self.get(DieselGeneratorCost))


class DieselGeneratorOperationsAndMaintenanceCostPerYear(V):

    section = 'system (off-grid)'
    option = 'diesel generator operations and maintenance cost per year'
    aliases = ['og_dsl_gntr_o_and_m_cst_pr_yr', 'og_dg_om']


    dependencies = [
        DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost,
        DieselGeneratorCost,
    ]
    units = 'dollars per year'

    def compute(self):
        return (
          self.get(DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost) * 
          self.get(DieselGeneratorCost))


class DieselGeneratorReplacementCostPerYear(V):

    section = 'system (off-grid)'
    option = 'diesel generator replacement cost per year'
    aliases = ['og_dsl_gntr_rpmt_cst_pr_yr', 'og_dg_rep']


    dependencies = [
        DieselGeneratorCost,
        DieselGeneratorLifetime,
    ]
    units = 'dollars per year'

    def compute(self):
        return (self.get(DieselGeneratorCost) / 
                float(self.get(DieselGeneratorLifetime)))


class DieselGeneratorEffectiveHoursOfOperationPerYear(V):

    section = 'system (off-grid)'
    option = 'diesel generator hours of operation per year (effective)'
    aliases = ['og_dsl_gntr_hrs_of_oprn_pr_yr_eff', 'og_dg_efhr']


    dependencies = [
        demand.ProjectedCommercialFacilityDemandPerYear,
        demand.ProjectedProductiveDemandPerYear,
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
        # Compute effectiveDemandPerYear and assume an off-grid diesel generator does NOT have distribution loss
        effectiveDemandPerYear = self.get(demand.ProjectedCommercialFacilityDemandPerYear) + self.get(demand.ProjectedProductiveDemandPerYear)
        # Return
        return max(self.get(DieselGeneratorMinimumHoursOfOperationPerYear), effectiveDemandPerYear / float(dieselGeneratorActualSystemCapacity))


class DieselFuelCostPerYear(V):

    section = 'system (off-grid)'
    option = 'diesel fuel cost per year'
    aliases = ['og_dsl_fuel_cst_pr_yr', 'og_fl']


    dependencies = [
        DieselFuelCostPerLiter,
        DieselFuelLitersConsumedPerKilowattHour,
        DieselGeneratorActualSystemCapacity,
        DieselGeneratorEffectiveHoursOfOperationPerYear,
    ]
    units = 'dollars per year'

    def compute(self):
        return (self.get(DieselFuelCostPerLiter) * 
                self.get(DieselFuelLitersConsumedPerKilowattHour) * 
                self.get(DieselGeneratorActualSystemCapacity) * 
                self.get(DieselGeneratorEffectiveHoursOfOperationPerYear))


#TODO:  Remove inherits from MiniGridSystemInitialCost?
class DieselComponentInitialCost(V):

    section = 'system (off-grid)'
    option = 'diesel component initial cost'
    aliases = ['og_dsl_cmpt_init_cst', 'og_d_ini']


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


#TODO:  Remove inherits from MiniGridSystemRecurringCostPerYear?
class DieselComponentRecurringCostPerYear(V):

    section = 'system (off-grid)'
    option = 'diesel component recurring cost per year'
    aliases = ['og_dsl_cmpt_rcrg_cst_pr_yr', 'og_d_rec']


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



# System costs


class OffGridSystemInitialCost(V):

    section = 'system (off-grid)'
    option = 'system initial cost'
    aliases = ['og_sys_init_cst', 'og_ini']


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
    aliases = ['og_sys_rcrg_cst_pr_yr', 'og_rec']


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
    aliases = ['og_sys_ndl_disc_cst', 'og_nod_d']


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


class OffGridSystemNodalDiscountedDieselFuelCost(V):

    section = 'system (off-grid)'
    option = 'system nodal discounted diesel fuel cost'
    aliases = ['og_sys_ndl_disc_dsl_fuel_cst', 'og_nod_ddfc']


    dependencies = [
        DieselFuelCostPerYear,
    ]

    def compute(self):
        return self.get(DieselFuelCostPerYear) * self.get(finance.DiscountedCashFlowFactor)


class OffGridSystemNodalDiscountedDieselCost(V):

    section = 'system (off-grid)'
    option = 'system nodal discounted diesel cost'
    aliases = ['og_sys_ndl_disc_dsl_cst', 'og_nod_ddc']


    dependencies = [
        demand.ProjectedNodalDemandPerYear,
        DieselComponentInitialCost,
        DieselComponentRecurringCostPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'dollars'

    def compute(self):
        if self.get(demand.ProjectedNodalDemandPerYear) == 0:
            return 0
        return self.get(DieselComponentInitialCost) + self.get(DieselComponentRecurringCostPerYear) * self.get(finance.DiscountedCashFlowFactor)


class OffGridSystemNodalLevelizedCost(V):

    section = 'system (off-grid)'
    option = 'system nodal levelized cost'
    aliases = ['og_sys_ndl_lvlzd_cst', 'og_nod_lev']


    dependencies = [
        demand.ProjectedNodalDiscountedDemand,
        OffGridSystemNodalDiscountedCost,
    ]
    units = 'dollars per kilowatt-hour'

    def compute(self):
        if self.get(demand.ProjectedNodalDiscountedDemand) == 0:
            return 0
        return self.get(OffGridSystemNodalDiscountedCost) / float(self.get(demand.ProjectedNodalDiscountedDemand))
