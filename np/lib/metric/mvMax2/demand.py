'Estimate electricity demand'
# Import custom modules
from np.lib.variable_store import Variable as V
from np.lib import store, curve
import finance
import demographics



# Social infrastructure count parameters


class HealthFacilityCountCurvePoints(V):

    section = 'demand (social infrastructure)'
    option = 'health facility count curve points (population and facility count)'
    aliases = ['he_cc_pts']
    c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
    default = '50 0.16; 500 1.6; 5000 5; 10000 20'
    units = 'population and facility count list'


class HealthFacilityCountCurveType(V):

    section = 'demand (social infrastructure)'
    option = 'health facility count curve type'
    aliases = ['he_cc_t']
    c = dict(parse=str, input=curve.inputCurveType)
    default = 'ZeroLogisticLinear'


class EducationFacilityCountCurvePoints(V):

    section = 'demand (social infrastructure)'
    option = 'education facility count curve points (population and facility count)'
    aliases = ['ed_cc_pts']
    c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
    default = '50 0.1; 500 1; 5000 3; 10000 15'
    units = 'population and facility count list'


class EducationFacilityCountCurveType(V):

    section = 'demand (social infrastructure)'
    option = 'education facility count curve type'
    aliases = ['ed_cc_t']
    c = dict(parse=str, input=curve.inputCurveType)
    default = 'ZeroLogisticLinear'


class CommercialFacilityCountCurvePoints(V):

    section = 'demand (social infrastructure)'
    option = 'commercial facility count curve points (population and facility count)'
    aliases = ['co_cc_pts']
    c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
    default = '50 0.12; 500 1.2; 5000 25; 10000 125'
    units = 'population and facility count list'


class CommercialFacilityCountCurveType(V):

    section = 'demand (social infrastructure)'
    option = 'commercial facility count curve type'
    aliases = ['co_cc_t']
    c = dict(parse=str, input=curve.inputCurveType)
    default = 'ZeroLogisticLinear'


class PublicLightingFacilityCountCurvePoints(V):

    section = 'demand (social infrastructure)'
    option = 'public lighting facility count curve points (population and facility count)'
    aliases = ['li_cc_pts']
    c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
    default = '50 0.1; 500 1; 5000 7; 10000 25'
    units = 'population and facility count list'


class PublicLightingFacilityCountCurveType(V):

    section = 'demand (social infrastructure)'
    option = 'public lighting facility count curve type'
    aliases = ['li_cc_t']
    c = dict(parse=str, input=curve.inputCurveType)
    default = 'ZeroLogisticLinear'



# Social infrastructure count derivatives


class HealthFacilityCountCurve(V):

    section = 'demand (social infrastructure)'
    option = 'health facility count curve'
    aliases = ['he_cc']
    c = dict(parse=curve.parse, format=curve.format)
    dependencies = [
        HealthFacilityCountCurveType,
        HealthFacilityCountCurvePoints,
    ]

    def compute(self):
        curveType = self.get(HealthFacilityCountCurveType)
        curvePoints = self.get(HealthFacilityCountCurvePoints)
        return curve.fit(curveType, curvePoints)


class ProjectedHealthFacilityCount(V):

    section = 'demand (social infrastructure)'
    option = 'projected health facility count'
    aliases = ['p_he']
    dependencies = [
        HealthFacilityCountCurve,
        demographics.ProjectedPopulationCount,
    ]
    units = 'health facility count'

    def compute(self):
        return self.get(HealthFacilityCountCurve).interpolate(self.get(demographics.ProjectedPopulationCount))


class EducationFacilityCountCurve(V):

    section = 'demand (social infrastructure)'
    option = 'education facility count curve'
    aliases = ['ed_cc']
    c = dict(parse=curve.parse, format=curve.format)
    dependencies = [
        EducationFacilityCountCurveType,
        EducationFacilityCountCurvePoints,
    ]

    def compute(self):
        curveType = self.get(EducationFacilityCountCurveType)
        curvePoints = self.get(EducationFacilityCountCurvePoints)
        return curve.fit(curveType, curvePoints)


class ProjectedEducationFacilityCount(V):

    section = 'demand (social infrastructure)'
    option = 'projected education facility count'
    aliases = ['p_ed']
    dependencies = [
        EducationFacilityCountCurve,
        demographics.ProjectedPopulationCount,
    ]
    units = 'education facility count'

    def compute(self):
        return self.get(EducationFacilityCountCurve).interpolate(self.get(demographics.ProjectedPopulationCount))


class CommercialFacilityCountCurve(V):

    section = 'demand (social infrastructure)'
    option = 'commercial facility count curve'
    aliases = ['co_cc']
    c = dict(parse=curve.parse, format=curve.format)
    dependencies = [
        CommercialFacilityCountCurveType,
        CommercialFacilityCountCurvePoints,
    ]

    def compute(self):
        curveType = self.get(CommercialFacilityCountCurveType)
        curvePoints = self.get(CommercialFacilityCountCurvePoints)
        return curve.fit(curveType, curvePoints)


class ProjectedCommercialFacilityCount(V):

    section = 'demand (social infrastructure)'
    option = 'projected commercial facility count'
    aliases = ['p_co']
    dependencies = [
        CommercialFacilityCountCurve,
        demographics.ProjectedPopulationCount,
    ]
    units = 'commercial facility count'

    def compute(self):
        return self.get(CommercialFacilityCountCurve).interpolate(self.get(demographics.ProjectedPopulationCount))


class PublicLightingFacilityCountCurve(V):

    section = 'demand (social infrastructure)'
    option = 'public lighting facility count curve'
    aliases = ['li_cc']
    c = dict(parse=curve.parse, format=curve.format)
    dependencies = [
        PublicLightingFacilityCountCurveType,
        PublicLightingFacilityCountCurvePoints,
    ]

    def compute(self):
        curveType = self.get(PublicLightingFacilityCountCurveType)
        curvePoints = self.get(PublicLightingFacilityCountCurvePoints)
        return curve.fit(curveType, curvePoints)


class ProjectedPublicLightingFacilityCount(V):

    section = 'demand (social infrastructure)'
    option = 'projected public lighting facility count'
    aliases = ['p_li']
    dependencies = [
        PublicLightingFacilityCountCurve,
        demographics.ProjectedPopulationCount,
    ]
    units = 'public lighting facility count'

    def compute(self):
        return self.get(PublicLightingFacilityCountCurve).interpolate(self.get(demographics.ProjectedPopulationCount))



# Household demand parameters


class HouseholdUnitDemandPerHouseholdPerYear(V):

    section = 'demand (household)'
    option = 'household unit demand per household per year'
    aliases = ['ho_dc_unit']
    default = 0 # 100
    units = 'kilowatt-hours per year'


class HouseholdDemandCurvePoints(V):

    section = 'demand (household)'
    option = 'demand curve points (population and multiplier)'
    aliases = ['ho_dc_pts']
    c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
    default = '500 1; 1000 1.56; 5000 6.16; 10000 11.5'
    units = 'population and multiplier list'


class HouseholdDemandCurveType(V):

    section = 'demand (household)'
    option = 'demand curve type'
    aliases = ['ho_dc_t']
    c = dict(parse=str, input=curve.inputCurveType)
    default = 'ZeroLogisticLinear'



# Household demand derivatives


class HouseholdDemandCurve(V):

    section = 'demand (household)'
    option = 'demand curve'
    aliases = ['ho_dc']
    c = dict(parse=curve.parse, format=curve.format)
    dependencies = [
        HouseholdDemandCurveType,
        HouseholdDemandCurvePoints,
    ]

    def compute(self):
        curveType = self.get(HouseholdDemandCurveType)
        curvePoints = self.get(HouseholdDemandCurvePoints)
        return curve.fit(curveType, curvePoints)


class ProjectedHouseholdDemandPerYear(V):

    section = 'demand (household)'
    option = 'projected household demand per year'
    aliases = ['p_dem_ho']
    dependencies = [
        finance.ElectricityDemandMultiplier,
        HouseholdDemandCurve,
        HouseholdUnitDemandPerHouseholdPerYear,
        demographics.ProjectedPopulationCount,
        demographics.ProjectedHouseholdCount,
    ]
    units = 'kilowatt-hours per year'

    def compute(self):
        return self.get(finance.ElectricityDemandMultiplier) * self.get(HouseholdDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(HouseholdUnitDemandPerHouseholdPerYear) * self.get(demographics.ProjectedHouseholdCount)



# Productive demand parameters


class ProductiveUnitDemandPerHouseholdPerYear(V):

    section = 'demand (productive)'
    option = 'productive unit demand per household per year'
    aliases = ['pr_dc_unit']
    default = 0 # 19.5
    units = 'kilowatt-hours per year'


class ProductiveDemandCurvePoints(V):

    section = 'demand (productive)'
    option = 'demand curve points (population and multiplier)'
    aliases = ['pr_dc_pts']
    c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
    default = '500 1; 1000 3.06; 5000 3.57; 10000 5.10'
    units = 'population and multiplier list'


class ProductiveDemandCurveType(V):

    section = 'demand (productive)'
    option = 'demand curve type'
    aliases = ['pr_dc_t']
    c = dict(parse=str, input=curve.inputCurveType)
    default = 'ZeroLogisticLinear'



# Productive demand derivatives


class ProductiveDemandCurve(V):

    section = 'demand (productive)'
    option = 'demand curve'
    aliases = ['pr_dc']
    c = dict(parse=curve.parse, format=curve.format)
    dependencies = [
        ProductiveDemandCurveType,
        ProductiveDemandCurvePoints,
    ]

    def compute(self):
        curveType = self.get(ProductiveDemandCurveType)
        curvePoints = self.get(ProductiveDemandCurvePoints)
        return curve.fit(curveType, curvePoints)


class ProjectedProductiveDemandPerYear(V):
    """
    Productive demand is power for community resources such as water pumps
    and grinding mills.  By estimating productive demand on a per household 
    basis, we do not have to estimate the number of water pumps or 
    grinding mills that are shared by a village.  The number of water pumps
    or grinding mills is generally smaller than the number of households.
    """

    section = 'demand (productive)'
    option = 'projected productive demand'
    aliases = ['p_dem_pr']
    dependencies = [
        finance.ElectricityDemandMultiplier,
        ProductiveDemandCurve,
        ProductiveUnitDemandPerHouseholdPerYear,
        demographics.ProjectedPopulationCount,
        demographics.ProjectedHouseholdCount,
    ]
    units = 'kilowatt-hours per year'

    def compute(self):
        return self.get(finance.ElectricityDemandMultiplier) * self.get(ProductiveDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(ProductiveUnitDemandPerHouseholdPerYear) * self.get(demographics.ProjectedHouseholdCount)



# Social infrastructure demand parameters


class HealthFacilityUnitDemandPerHealthFacilityPerYear(V):

    section = 'demand (social infrastructure)'
    option = 'health facility unit demand per health facility per year'
    aliases = ['he_dc_unit']
    default = 0 # 1000
    units = 'kilowatt-hours per year'


class EducationFacilityUnitDemandPerEducationFacilityPerYear(V):

    section = 'demand (social infrastructure)'
    option = 'education facility unit demand per education facility per year'
    aliases = ['ed_dc_unit']
    default = 0 # 1200
    units = 'kilowatt-hours per year'


class CommercialFacilityUnitDemandPerCommercialFacilityPerYear(V):

    section = 'demand (social infrastructure)'
    option = 'commercial facility unit demand per commercial facility per year'
    aliases = ['co_dc_unit']
    default = 0 # 250
    units = 'kilowatt-hours per year'


class PublicLightingFacilityUnitDemandPerPublicLightingFacilityPerYear(V):

    section = 'demand (social infrastructure)'
    option = 'public lighting facility unit demand per public lighting facility per year'
    aliases = ['li_dc_unit']
    default = 0 # 102
    units = 'kilowatt-hours per year'


class SocialInfrastructureDemandCurvePoints(V):

    section = 'demand (social infrastructure)'
    option = 'demand curve points (population and multiplier)'
    aliases = ['so_dc_pts']
    c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
    default = '500 1; 1000 1.5; 5000 2.25; 10000 3.375' 
    units = 'population and multiplier list'


class SocialInfrastructureDemandCurveType(V):

    section = 'demand (social infrastructure)'
    option = 'demand curve type'
    aliases = ['so_dc_t']
    c = dict(parse=str, input=curve.inputCurveType)
    default = 'ZeroLogisticLinear'



# Social infrastructure demand derivatives


class SocialInfrastructureDemandCurve(V):

    section = 'demand (social infrastructure)'
    option = 'demand curve'
    aliases = ['so_dc']
    c = dict(parse=curve.parse, format=curve.format)
    dependencies = [
        SocialInfrastructureDemandCurveType,
        SocialInfrastructureDemandCurvePoints,
    ]

    def compute(self):
        curveType = self.get(SocialInfrastructureDemandCurveType)
        curvePoints = self.get(SocialInfrastructureDemandCurvePoints)
        return curve.fit(curveType, curvePoints)


class ProjectedHealthFacilityDemandPerYear(V):

    section = 'demand (social infrastructure)'
    option = 'projected health facility demand per year'
    aliases = ['p_dem_he']
    dependencies = [
        finance.ElectricityDemandMultiplier,
        SocialInfrastructureDemandCurve,
        HealthFacilityUnitDemandPerHealthFacilityPerYear,
        demographics.ProjectedPopulationCount,
        ProjectedHealthFacilityCount,
    ]
    units = 'kilowatt-hours per year'

    def compute(self):
        return self.get(finance.ElectricityDemandMultiplier) * self.get(SocialInfrastructureDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(HealthFacilityUnitDemandPerHealthFacilityPerYear) * self.get(ProjectedHealthFacilityCount)


class ProjectedEducationFacilityDemandPerYear(V):

    section = 'demand (social infrastructure)'
    option = 'projected education facility demand per year'
    aliases = ['p_dem_ed']
    dependencies = [
        finance.ElectricityDemandMultiplier,
        SocialInfrastructureDemandCurve,
        EducationFacilityUnitDemandPerEducationFacilityPerYear,
        demographics.ProjectedPopulationCount,
        ProjectedEducationFacilityCount,
    ]
    units = 'kilowatt-hours per year'

    def compute(self):
        return self.get(finance.ElectricityDemandMultiplier) * self.get(SocialInfrastructureDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(EducationFacilityUnitDemandPerEducationFacilityPerYear) * self.get(ProjectedEducationFacilityCount)


class ProjectedCommercialFacilityDemandPerYear(V):

    section = 'demand (social infrastructure)'
    option = 'projected commercial facility demand per year'
    aliases = ['p_dem_co']
    dependencies = [
        finance.ElectricityDemandMultiplier,
        SocialInfrastructureDemandCurve,
        CommercialFacilityUnitDemandPerCommercialFacilityPerYear,
        demographics.ProjectedPopulationCount,
        ProjectedCommercialFacilityCount,
    ]
    units = 'kilowatt-hours per year'

    def compute(self):
        return self.get(finance.ElectricityDemandMultiplier) * self.get(SocialInfrastructureDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(CommercialFacilityUnitDemandPerCommercialFacilityPerYear) * self.get(ProjectedCommercialFacilityCount)


class ProjectedPublicLightingFacilityDemandPerYear(V):

    section = 'demand (social infrastructure)'
    option = 'projected public lighting facility demand per year'
    aliases = ['p_dem_li']
    dependencies = [
        finance.ElectricityDemandMultiplier,
        SocialInfrastructureDemandCurve,
        PublicLightingFacilityUnitDemandPerPublicLightingFacilityPerYear,
        demographics.ProjectedPopulationCount,
        ProjectedPublicLightingFacilityCount,
    ]
    units = 'kilowatt-hours per year'

    def compute(self):
        return self.get(finance.ElectricityDemandMultiplier) * self.get(SocialInfrastructureDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(PublicLightingFacilityUnitDemandPerPublicLightingFacilityPerYear) * self.get(ProjectedPublicLightingFacilityCount)


class ProjectedNodalDemandPerYear(V):

    section = 'demand'
    option = 'projected nodal demand per year'
    aliases = ['p_dem']
    dependencies = [
        ProjectedHouseholdDemandPerYear,
        ProjectedProductiveDemandPerYear,
        ProjectedHealthFacilityDemandPerYear,
        ProjectedEducationFacilityDemandPerYear,
        ProjectedCommercialFacilityDemandPerYear,
        ProjectedPublicLightingFacilityDemandPerYear,
    ]
    units = 'kilowatt-hours per year'

    def compute(self):
        return sum([
            self.get(ProjectedHouseholdDemandPerYear),
            self.get(ProjectedProductiveDemandPerYear),
            self.get(ProjectedHealthFacilityDemandPerYear),
            self.get(ProjectedEducationFacilityDemandPerYear),
            self.get(ProjectedCommercialFacilityDemandPerYear),
            self.get(ProjectedPublicLightingFacilityDemandPerYear),
        ])


class ProjectedNodalDiscountedDemand(V):
    """
    Note that we are overestimating nodal demand aggregated over the time horizon
    since we are using the projected demand at the end of the time horizon as the
    recurring demand per year, which in real-life should scale year by year.
    """

    section = 'demand'
    option = 'projected nodal discounted demand'
    aliases = ['p_dem_d']
    dependencies = [
        ProjectedNodalDemandPerYear,
        finance.DiscountedCashFlowFactor,
    ]
    units = 'kilowatt-hours'

    def compute(self):
        return self.get(ProjectedNodalDemandPerYear) * self.get(finance.DiscountedCashFlowFactor)



# Peak demand parameters


class RuralPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours(V):

    section = 'demand (peak)'
    option = 'peak demand as fraction of nodal demand occurring during peak hours (rural)'
    aliases = ['pkdemf_r']
    default = 0.4


class UrbanPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours(V):

    section = 'demand (peak)'
    option = 'peak demand as fraction of nodal demand occurring during peak hours (urban)'
    aliases = ['pkdemf_u']
    default = 0.4


class PeakElectricalHoursOfOperationPerYear(V):

    section = 'demand (peak)'
    option = 'peak electrical hours of operation per year'
    aliases = ['pkhr']
    c = dict(check=store.assertPositive)
    default = 1460
    units = 'hours per year'



# Peak demand derivatives


class PeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours(V):

    section = 'demand (peak)'
    option = 'peak demand as fraction of nodal demand occurring during peak hours'
    aliases = ['pkdemf']
    dependencies = [
        RuralPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours,
        demographics.IsRural,
        UrbanPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours,
    ]

    def compute(self):
        return self.get(RuralPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours) if self.get(demographics.IsRural) else self.get(UrbanPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours)


class DemandToPeakDemandConversionFactor(V):

    section = 'demand (peak)'
    option = 'demand to peak demand conversion factor'
    aliases = ['dem_pkdemf']
    dependencies = [
        PeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours,
        PeakElectricalHoursOfOperationPerYear,
    ]

    def compute(self):
        return self.get(PeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours) / float(self.get(PeakElectricalHoursOfOperationPerYear))


class ProjectedPeakHouseholdDemand(V):

    section = 'demand (peak)'
    option = 'projected peak household demand'
    aliases = ['p_pkdem_ho']
    dependencies = [
        ProjectedHouseholdDemandPerYear,
        DemandToPeakDemandConversionFactor,
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(ProjectedHouseholdDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)


class ProjectedPeakProductiveDemand(V):

    section = 'demand (peak)'
    option = 'projected peak productive demand'
    aliases = ['p_pkdem_pr']
    dependencies = [
        ProjectedProductiveDemandPerYear,
        DemandToPeakDemandConversionFactor,
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(ProjectedProductiveDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)


class ProjectedPeakHealthFacilityDemand(V):

    section = 'demand (peak)'
    option = 'projected peak health facility demand'
    aliases = ['p_pkdem_he']
    dependencies = [
        ProjectedHealthFacilityDemandPerYear,
        DemandToPeakDemandConversionFactor,
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(ProjectedHealthFacilityDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)


class ProjectedPeakEducationFacilityDemand(V):

    section = 'demand (peak)'
    option = 'projected peak education facility demand'
    aliases = ['p_pkdem_ed']
    dependencies = [
        ProjectedEducationFacilityDemandPerYear,
        DemandToPeakDemandConversionFactor,
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(ProjectedEducationFacilityDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)


class ProjectedPeakCommercialFacilityDemand(V):

    section = 'demand (peak)'
    option = 'projected peak commercial facility demand'
    aliases = ['p_pkdem_co']
    dependencies = [
        ProjectedCommercialFacilityDemandPerYear,
        DemandToPeakDemandConversionFactor,
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(ProjectedCommercialFacilityDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)


class ProjectedPeakPublicLightingFacilityDemand(V):

    section = 'demand (peak)'
    option = 'projected peak public lighting facility demand'
    aliases = ['p_pkdem_li']
    dependencies = [
        ProjectedPublicLightingFacilityDemandPerYear,
        DemandToPeakDemandConversionFactor,
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(ProjectedPublicLightingFacilityDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)


class ProjectedPeakNodalDemand(V):

    section = 'demand (peak)'
    option = 'projected peak nodal demand'
    aliases = ['p_pkdem']
    dependencies = [
        ProjectedNodalDemandPerYear,
        DemandToPeakDemandConversionFactor,
    ]
    units = 'kilowatts'

    def compute(self):
        return self.get(ProjectedNodalDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)
