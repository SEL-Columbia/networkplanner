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
    aliases = ['OG_PkSunHrsPrYr', 'pksu_hr']

    short_section = 'OG'
    short_option = 'PkSunHrsPrYr'

    c = dict(check=store.assertPositive)
    default = 1320
    units = 'hours per year'


class PhotovoltaicPanelAvailableSystemCapacities(V):

    section = 'system (off-grid)'
    option = 'available system capacities (photovoltaic panel)'
    aliases = ['OG_AvblSysCapPVPnl', 'og_pp_cps']

    short_section = 'OG'
    short_option = 'AvblSysCapPVPnl'

    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1.5 1.0 0.4 0.15 0.075 0.05'
    units = 'kilowatts list'


class PhotovoltaicPanelCostPerPhotovoltaicComponentKilowatt(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel cost per photovoltaic component kilowatt'
    aliases = ['OG_PVPnlCstPrPVCmptkW', 'og_pp_ckw']

    short_section = 'OG'
    short_option = 'PVPnlCstPrPVCmptkW'

    default = 6000
    units = 'dollars per kilowatt'


class PhotovoltaicBalanceCostAsFractionOfPanelCost(V):

    section = 'system (off-grid)'
    option = 'photovoltaic balance cost as fraction of panel cost'
    aliases = ['OG_PVBalCstAsFctnOfPnlCst', 'og_px_cf']

    short_section = 'OG'
    short_option = 'PVBalCstAsFctnOfPnlCst'

    default = 0.5


class PhotovoltaicBatteryKilowattHoursPerPhotovoltaicComponentKilowatt(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery kilowatt-hours per photovoltaic component kilowatt'
    aliases = ['OG_PVBattkWHrPrPVCmptkW', 'og_pb_hkw']

    short_section = 'OG'
    short_option = 'PVBattkWHrPrPVCmptkW'

    default = 5
    units = 'kilowatt-hours per kilowatt'


class PhotovoltaicBatteryCostPerKilowattHour(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery cost per kilowatt-hour'
    aliases = ['OG_PVBattCstPrkWHr', 'og_pb_ckwh']

    short_section = 'OG'
    short_option = 'PVBattCstPrkWHr'

    default = 400
    units = 'dollars per kilowatt-hour'


class PhotovoltaicPanelLifetime(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel lifetime'
    aliases = ['OG_PVPnlLife', 'og_pp_life']

    short_section = 'OG'
    short_option = 'PVPnlLife'

    c = dict(check=store.assertPositive)
    default = 30
    units = 'years'


class PhotovoltaicBalanceLifetime(V):

    section = 'system (off-grid)'
    option = 'photovoltaic balance lifetime'
    aliases = ['OG_PVBalLife', 'og_px_life']

    short_section = 'OG'
    short_option = 'PVBalLife'

    c = dict(check=store.assertPositive)
    default = 10
    units = 'years'


class PhotovoltaicBatteryLifetime(V):

    section = 'system (off-grid)'
    option = 'photovoltaic battery lifetime'
    aliases = ['OG_PVBattLife', 'og_pb_life']

    short_section = 'OG'
    short_option = 'PVBattLife'

    c = dict(check=store.assertPositive)
    default = 3
    units = 'years'


class PhotovoltaicComponentEfficiencyLoss(V):

    section = 'system (off-grid)'
    option = 'photovoltaic component efficiency loss'
    aliases = ['OG_PVCmptEfcyLss', 'og_p_loss']

    short_section = 'OG'
    short_option = 'PVCmptEfcyLss'

    c = dict(check=store.assertLessThanOne)
    default = 0.1
    units = 'fraction'


class PhotovoltaicComponentOperationsAndMaintenanceCostPerYearAsFractionOfComponentCost(V):

    section = 'system (off-grid)'
    option = 'photovoltaic component operations and maintenance cost per year as fraction of component cost'
    aliases = ['OG_PVCmptOandMCstPrYrAsFctnOfCmptCst', 'og_p_omf']

    short_section = 'OG'
    short_option = 'PVCmptOandMCstPrYrAsFctnOfCmptCst'

    default = 0.05


class DieselGeneratorAvailableSystemCapacities(V):

    section = 'system (off-grid)'
    option = 'available system capacities (diesel generator)'
    aliases = ['OG_AvblSysCapDslGntr', 'og_dg_cps']

    short_section = 'OG'
    short_option = 'AvblSysCapDslGntr'

    c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
    default = '1000 750 500 400 200 150 100 70 32 19 12 10 8 6'
    units = 'kilowatts list'


class DieselGeneratorCostPerDieselSystemKilowatt(V):

    section = 'system (off-grid)'
    option = 'diesel generator cost per diesel system kilowatt'
    aliases = ['OG_DslGntrCstPrDslSyskW', 'og_dg_ck']

    short_section = 'OG'
    short_option = 'DslGntrCstPrDslSyskW'

    default = 150
    units = 'dollars per kilowatt'

class DieselGeneratorInstallationCostAsFractionOfGeneratorCost(V):

    section = 'system (off-grid)'
    aliases = ['OG_DslGntrInstCstAsFctnOfGntrCst', 'og_dg_if']

    short_section = 'OG'
    short_option = 'DslGntrInstCstAsFctnOfGntrCst'

    option = 'diesel generator installation cost as fraction of generator cost'
    default = 0.25


class DieselGeneratorLifetime(V):

    section = 'system (mini-grid)'
    option = 'diesel generator lifetime'
    aliases = ['MG_DslGntrLife', 'og_dg_life']

    short_section = 'MG'
    short_option = 'DslGntrLife'

    c = dict(check=store.assertPositive)
    default = 5
    units = 'years'


class DieselFuelCostPerLiter(V):

    section = 'system (off-grid)'
    option = 'diesel fuel cost per liter'
    aliases = ['OG_DslCstPrLtr', 'og_fl_cl']

    short_section = 'OG'
    short_option = 'DslCstPrLtr'

    default = 1.08
    units = 'dollars per liter'


class DieselFuelLitersConsumedPerKilowattHour(V):

    section = 'system (off-grid)'
    option = 'diesel fuel liters consumed per kilowatt-hour'
    aliases = ['OG_DslLtrCsmdPrkWHr', 'og_fl_lkwh']

    short_section = 'OG'
    short_option = 'DslLtrCsmdPrkWHr'

    default = 0.5
    units = 'liters per kilowatt-hour'


class DieselGeneratorMinimumHoursOfOperationPerYear(V):

    section = 'system (off-grid)'
    option = 'diesel generator hours of operation per year (minimum)'
    aliases = ['OG_DslGntrHrsOfOprnPrYrMin', 'og_dg_mnhr']

    short_section = 'OG'
    short_option = 'DslGntrHrsOfOprnPrYrMin'

    default = 1460
    units = 'hours per year'


class DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost(V):

    section = 'system (off-grid)'
    option = 'diesel generator operations and maintenance cost per year as fraction of generator cost'
    aliases = ['OG_DslGntrOandMCstPrYrAsFctnOfGntrCst', 'og_dg_omf']

    short_section = 'OG'
    short_option = 'DslGntrOandMCstPrYrAsFctnOfGntrCst'

    default = 0.01


# Photovoltaic intermediates


class PhotovoltaicPanelDesiredSystemCapacity(V):

    section = 'system (off-grid)'
    option = 'photovoltaic panel desired capacity'
    aliases = ['OG_PVPnlDsrdCpty', 'og_pp_dcp']

    short_section = 'OG'
    short_option = 'PVPnlDsrdCpty'

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
    aliases = ['OG_PVPnlActlCptyCts', 'og_pp_acps']

    short_section = 'OG'
    short_option = 'PVPnlActlCptyCts'

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
    aliases = ['OG_PVPnlActlCpty', 'og_pp_acp']

    short_section = 'OG'
    short_option = 'PVPnlActlCpty'

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
    aliases = ['OG_PVPnlCst', 'og_pp_ini']

    short_section = 'OG'
    short_option = 'PVPnlCst'

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
    aliases = ['OG_PVPnlRpmtCstPrYr', 'og_pp_rep']

    short_section = 'OG'
    short_option = 'PVPnlRpmtCstPrYr'

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
    aliases = ['OG_PVBattCst', 'og_pb_ini']

    short_section = 'OG'
    short_option = 'PVBattCst'

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
    aliases = ['OG_PVBattRpmtCstPrYr', 'og_pb_rep']

    short_section = 'OG'
    short_option = 'PVBattRpmtCstPrYr'

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
    aliases = ['OG_PVBalCst', 'og_px_ini']

    short_section = 'OG'
    short_option = 'PVBalCst'

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
    aliases = ['OG_PVBalRpmtCstPrYr', 'og_px_rep']

    short_section = 'OG'
    short_option = 'PVBalRpmtCstPrYr'

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
    aliases = ['OG_PVCmptInitCst', 'og_p_ini']

    short_section = 'OG'
    short_option = 'PVCmptInitCst'

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
    aliases = ['OG_PVCmptOandMCstPrYr', 'og_p_om']

    short_section = 'OG'
    short_option = 'PVCmptOandMCstPrYr'

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
    aliases = ['OG_PVCmptRcrgCstPrYr', 'og_p_rec']

    short_section = 'OG'
    short_option = 'PVCmptRcrgCstPrYr'

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
    aliases = ['OG_DslGntrDsrdSysCpty', 'og_dg_dcp']

    short_section = 'OG'
    short_option = 'DslGntrDsrdSysCpty'

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
    aliases = ['OG_DslGntrActlSysCptyCts', 'og_dg_acps']

    short_section = 'OG'
    short_option = 'DslGntrActlSysCptyCts'

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
    aliases = ['OG_DslGntrActlSysCpty', 'og_dg_acp']

    short_section = 'OG'
    short_option = 'DslGntrActlSysCpty'

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
    aliases = ['OG_DslGntrCst', 'og_dg_ini']

    short_section = 'OG'
    short_option = 'DslGntrCst'

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
    aliases = ['OG_DslGntrInstCst', 'og_dg_i']

    short_section = 'OG'
    short_option = 'DslGntrInstCst'

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
    aliases = ['OG_DslGntrOandMCstPrYr', 'og_dg_om']

    short_section = 'OG'
    short_option = 'DslGntrOandMCstPrYr'

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
    aliases = ['OG_DslGntrRpmtCstPrYr', 'og_dg_rep']

    short_section = 'OG'
    short_option = 'DslGntrRpmtCstPrYr'

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
    aliases = ['OG_DslGntrHrsOfOprnPrYrEff', 'og_dg_efhr']

    short_section = 'OG'
    short_option = 'DslGntrHrsOfOprnPrYrEff'

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
    aliases = ['OG_DslFuelCstPrYr', 'og_fl']

    short_section = 'OG'
    short_option = 'DslFuelCstPrYr'

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
    aliases = ['OG_DslCmptInitCst', 'og_d_ini']

    short_section = 'OG'
    short_option = 'DslCmptInitCst'

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
    aliases = ['OG_DslCmptRcrgCstPrYr', 'og_d_rec']

    short_section = 'OG'
    short_option = 'DslCmptRcrgCstPrYr'

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
    aliases = ['OG_SysInitCst', 'og_ini']

    short_section = 'OG'
    short_option = 'SysInitCst'

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
    aliases = ['OG_SysRcrgCstPrYr', 'og_rec']

    short_section = 'OG'
    short_option = 'SysRcrgCstPrYr'

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
    aliases = ['OG_SysNdlDsctdCst', 'og_nod_d']

    short_section = 'OG'
    short_option = 'SysNdlDsctdCst'

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
    aliases = ['OG_SysNdlDsctdDslFuelCst', 'og_nod_ddfc']

    short_section = 'OG'
    short_option = 'SysNdlDsctdDslFuelCst'

    dependencies = [
        DieselFuelCostPerYear,
    ]

    def compute(self):
        return self.get(DieselFuelCostPerYear) * self.get(finance.DiscountedCashFlowFactor)


class OffGridSystemNodalDiscountedDieselCost(V):

    section = 'system (off-grid)'
    option = 'system nodal discounted diesel cost'
    aliases = ['OG_SysNdlDsctdDslCst', 'og_nod_ddc']

    short_section = 'OG'
    short_option = 'SysNdlDsctdDslCst'

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
    aliases = ['OG_SysNdlLvlzdCst', 'og_nod_lev']

    short_section = 'OG'
    short_option = 'SysNdlLvlzdCst'

    dependencies = [
        demand.ProjectedNodalDiscountedDemand,
        OffGridSystemNodalDiscountedCost,
    ]
    units = 'dollars per kilowatt-hour'

    def compute(self):
        if self.get(demand.ProjectedNodalDiscountedDemand) == 0:
            return 0
        return self.get(OffGridSystemNodalDiscountedCost) / float(self.get(demand.ProjectedNodalDiscountedDemand))
