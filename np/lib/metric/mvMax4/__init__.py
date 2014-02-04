'Compute the maximum length of medium voltage line for which grid extension is cheaper than standalone options'
# Import custom modules
from np.lib.variable_store import VariableStore as VS, Variable as V
from np.lib import store
import finance
import demographics
import demand
import costDistribution
import costOffGrid
import costMiniGrid
import costGrid



# Variable

class Metric(V):
    'Maximum length of medium voltage line for which grid extension is cheaper than standalone options'

    section = 'metric'
    option = 'maximum length of medium voltage line extension'
    aliases = ['metric_mv_max', 'mvmax']
    dependencies = [
        costOffGrid.OffGridSystemNodalDiscountedCost,
        costOffGrid.OffGridSystemNodalLevelizedCost,
        costMiniGrid.MiniGridSystemNodalDiscountedCost,
        costMiniGrid.MiniGridSystemNodalLevelizedCost,
        costGrid.GridInternalSystemNodalDiscountedCost,
        costGrid.GridInternalSystemNodalLevelizedCost,
        costGrid.GridExternalSystemNodalDiscountedCostPerMeter,
    ]
    units = 'meters'

    def compute(self):
        # Compute levelized costs
        self.get(costOffGrid.OffGridSystemNodalLevelizedCost)
        self.get(costMiniGrid.MiniGridSystemNodalLevelizedCost)
        self.get(costGrid.GridInternalSystemNodalLevelizedCost)
        # Compute the cost of the cheapest standalone option for the node
        standaloneCost = min(
            self.get(costOffGrid.OffGridSystemNodalDiscountedCost),
            self.get(costMiniGrid.MiniGridSystemNodalDiscountedCost))
        # Compute the (non-negative) amount of money we have left to spend on grid extension
        gridExternalBudget = max(0, standaloneCost - self.get(costGrid.GridInternalSystemNodalDiscountedCost))
        # Compute the length of line we are allowed for grid extension
        return gridExternalBudget / float(self.get(costGrid.GridExternalSystemNodalDiscountedCostPerMeter))


class System(V):

    section = 'metric'
    option = 'system'
    aliases = ['metric_sys', 'system']
    c = dict(parse=str)
    dependencies = [
        demand.ProjectedNodalDemandPerYear,
        costMiniGrid.MiniGridSystemNodalDiscountedCost,
        costOffGrid.OffGridSystemNodalDiscountedCost,
    ]

    def compute(self):
        # If the demand is positive,
        if self.get(demand.ProjectedNodalDemandPerYear) == 0:
            return 'unelectrified'
        # If grid is chosen,
        elif self.state[0].isNodeConnected(self.state[1]):
            return 'grid'
        # If mini-grid is chosen,
        elif self.get(costMiniGrid.MiniGridSystemNodalDiscountedCost) < self.get(costOffGrid.OffGridSystemNodalDiscountedCost):
            return 'mini-grid'
        # If off-grid is chosen,
        else:
            return 'off-grid'



# Aggregate

class OffGridSystemTotal(V):

    section = 'system (off-grid)'
    option = 'system total'
    aliases = ['og_sys_tot', 'og_ct']
    default = 0
    units = 'count'

    def aggregate(self, childVS):
        # If the system is off-grid,
        if childVS.get(System)[0] == 'o':
            # Update
            self.value += 1


class OffGridSystemTotalDiscountedDemand(V):

    section = 'system (off-grid)'
    option = 'system total discounted demand'
    aliases = ['og_sys_tot_disc_dmd', 'og_dem_d']
    default = 0
    units = 'kilowatt-hours'

    def aggregate(self, childVS):
        # If the system is off-grid,
        if childVS.get(System)[0] == 'o':
            # Update
            self.value += childVS.get(demand.ProjectedNodalDiscountedDemand)


class OffGridSystemTotalDiscountedDieselCost(V):

    section = 'system (off-grid)'
    option = 'system total discounted diesel cost'
    aliases = ['og_sys_tot_disc_dsl_cst', 'og_tot_ddc']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is off-grid,
        if childVS.get(System)[0] == 'o':
            # add up nodal diesel costs
            self.value += childVS.get(costOffGrid.OffGridSystemNodalDiscountedDieselCost) 


class OffGridSystemTotalDiscountedDieselFuelCost(V):

    section = 'system (off-grid)'
    option = 'system total discounted diesel fuel cost'
    aliases = ['og_sys_tot_disc_dsl_fuel_cst', 'og_tot_ddfc']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is off-grid,
        if childVS.get(System)[0] == 'o':
            # add up nodal diesel costs
            self.value += childVS.get(costOffGrid.OffGridSystemNodalDiscountedDieselFuelCost) 


class OffGridSystemTotalDiscountedCost(V):

    section = 'system (off-grid)'
    option = 'system total discounted cost'
    aliases = ['og_sys_tot_disc_cst', 'og_tot_d']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is off-grid,
        if childVS.get(System)[0] == 'o':
            # Update
            self.value += childVS.get(costOffGrid.OffGridSystemNodalDiscountedCost)


class OffGridSystemTotalLevelizedCost(V):

    section = 'system (off-grid)'
    option = 'system total levelized cost'
    aliases = ['og_sys_tot_lvlzd_cst', 'og_tot_lev']
    dependencies = [
        OffGridSystemTotalDiscountedDemand,
        OffGridSystemTotalDiscountedCost,
    ]
    units = 'dollars per kilowatt-hour'

    def compute(self):
        if self.get(OffGridSystemTotalDiscountedDemand) == 0:
            return 0
        return self.get(OffGridSystemTotalDiscountedCost) / float(self.get(OffGridSystemTotalDiscountedDemand))


class OffGridSystemTotalInitialCost(V):

    section = 'system (off-grid)'
    option = 'system total initial cost'
    aliases = ['og_sys_tot_init_cst', 'og_tot_i']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is off-grid,
        if childVS.get(System)[0] == 'o':
            # Update
            self.value += childVS.get(costOffGrid.OffGridSystemInitialCost)


class OffGridSystemTotalDiscountedRecurringCost(V):

    section = 'system (off-grid)'
    option = 'system total discounted recurring cost'
    aliases = ['og_sys_tot_disc_rcrg_cst', 'og_tot_drc']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is off-grid,
        if childVS.get(System)[0] == 'o':
            # Update
            self.value += ( \
                    childVS.get(costOffGrid.OffGridSystemRecurringCostPerYear) * \
                    childVS.get(finance.DiscountedCashFlowFactor))


class MiniGridSystemTotal(V):

    section = 'system (mini-grid)'
    option = 'system total'
    aliases = ['mg_sys_tot', 'mg_ct']
    default = 0
    units = 'count'

    def aggregate(self, childVS):
        # If the system is mini-grid,
        if childVS.get(System)[0] == 'm':
            # Update
            self.value += 1


class MiniGridSystemTotalDiscountedDieselFuelCost(V):

    section = 'system (mini-grid)'
    option = 'system total discounted diesel fuel cost'
    aliases = ['mg_sys_tot_disc_dsl_fuel_cst', 'mg_tot_ddfc']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is mini-grid,
        if childVS.get(System)[0] == 'm':
            # add up nodal diesel costs
            self.value += childVS.get(costMiniGrid.MiniGridSystemNodalDiscountedDieselFuelCost) 


class MiniGridSystemTotalDiscountedDieselCost(V):

    section = 'system (mini-grid)'
    option = 'system total discounted diesel cost'
    aliases = ['mg_tot_ddc']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is off-grid,
        if childVS.get(System)[0] == 'm':
            # add up nodal diesel costs
            self.value += childVS.get(costMiniGrid.MiniGridSystemNodalDiscountedDieselCost) 


class MiniGridSystemTotalDiscountedDemand(V):

    section = 'system (mini-grid)'
    option = 'system total discounted demand'
    aliases = ['mg_sys_tot_disc_dmd', 'mg_dem_d']
    default = 0
    units = 'kilowatt-hours'

    def aggregate(self, childVS):
        # If the system is mini-grid,
        if childVS.get(System)[0] == 'm':
            # Update
            self.value += childVS.get(demand.ProjectedNodalDiscountedDemand)


class MiniGridSystemTotalDiscountedCost(V):

    section = 'system (mini-grid)'
    option = 'system total discounted cost'
    aliases = ['mg_sys_tot_disc_cst', 'mg_tot_d']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is mini-grid,
        if childVS.get(System)[0] == 'm':
            # Update
            self.value += childVS.get(costMiniGrid.MiniGridSystemNodalDiscountedCost)


class MiniGridSystemTotalInitialCost(V):

    section = 'system (mini-grid)'
    option = 'system total initial cost'
    aliases = ['mg_sys_tot_init_cst', 'mg_tot_i']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is mini-grid,
        if childVS.get(System)[0] == 'm':
            # Update
            self.value += childVS.get(costMiniGrid.MiniGridSystemInitialCost)


class MiniGridSystemTotalDiscountedRecurringCost(V):

    section = 'system (mini-grid)'
    option = 'system total discounted recurring cost'
    aliases = ['mg_sys_tot_disc_rcrg_cst', 'mg_tot_drc']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # If the system is mini-grid,
        if childVS.get(System)[0] == 'm':
            # Update
            self.value += ( \
                    childVS.get(costMiniGrid.MiniGridSystemRecurringCostPerYear) * \
                    childVS.get(finance.DiscountedCashFlowFactor))


class MiniGridSystemTotalLevelizedCost(V):

    section = 'system (mini-grid)'
    option = 'system total levelized cost'
    aliases = ['mg_sys_tot_lvlzd_cst', 'mg_tot_lev']
    dependencies = [
        MiniGridSystemTotalDiscountedDemand,
        MiniGridSystemTotalDiscountedCost,
    ]
    units = 'dollars per kilowatt-hour'

    def compute(self):
        if self.get(MiniGridSystemTotalDiscountedDemand) == 0:
            return 0
        return self.get(MiniGridSystemTotalDiscountedCost) / float(self.get(MiniGridSystemTotalDiscountedDemand))


class GridSystemTotal(V):

    section = 'system (grid)'
    option = 'system total'
    aliases = ['gr_sys_tot', 'g_ct']
    default = 0
    units = 'count'

    def aggregate(self, childVS):
        # If the system is grid,
        if childVS.get(System)[0] == 'g':
            # Update
            self.value += 1


class GridSystemTotalDiscountedDemand(V):

    section = 'system (grid)'
    option = 'system total discounted demand'
    aliases = ['gr_sys_tot_disc_dmd', 'gr_dem_d']
    default = 0
    units = 'kilowatt-hours'

    def aggregate(self, childVS):
        # Get
        childDataset = childVS.state[0]
        childNode = childVS.state[1]
        # If the system is grid and we are connecting a node that was not in the existing grid,
        if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
            # Update
            self.value += childVS.get(demand.ProjectedNodalDiscountedDemand)


class GridSystemTotalExternalInitialCost(V):

    section = 'system (grid)'
    option = 'system total external initial cost'
    aliases = ['gr_sys_tot_ext_init_cst', 'gr_tot_ext_ic']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # Get
        childDataset = childVS.state[0]
        childNode = childVS.state[1]
        # If the system is grid and we are connecting a node that was not in the existing grid,
        if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
            # Get half the length of all new connections to the node
            newConnections = childDataset.cycleConnections(childNode, is_existing=False)
            newConnectionLengthHalved = sum(x.weight for x in newConnections) / 2.
            # Get initial external cost
            externalCostPerMeter = childVS.get(costGrid.GridExternalSystemInitialCostPerMeter)
            externalCost = externalCostPerMeter * newConnectionLengthHalved
            # Add internal and external cost
            self.value += externalCost


class GridSystemTotalExternalDiscountedRecurringCost(V):

    section = 'system (grid)'
    option = 'system total external discounted recurring cost'
    aliases = ['gr_sys_tot_ext_disc_rcrg_cst', 'gr_tot_ext_drc']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # Get
        childDataset = childVS.state[0]
        childNode = childVS.state[1]
        # If the system is grid and we are connecting a node that was not in the existing grid,
        if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
            # Get half the length of all new connections to the node
            newConnections = childDataset.cycleConnections(childNode, is_existing=False)
            newConnectionLengthHalved = sum(x.weight for x in newConnections) / 2.
            # Get discounted external cost
            discountedExternalCostPerMeter = childVS.get(costGrid.GridExternalSystemNodalDiscountedRecurringCostPerMeter)
            externalRecurringCost = discountedExternalCostPerMeter * newConnectionLengthHalved
            self.value += externalRecurringCost


class GridSystemTotalDiscountedCost(V):

    section = 'system (grid)'
    option = 'system total discounted cost'
    aliases = ['gr_sys_tot_disc_cst', 'gr_tot_d']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # Get
        childDataset = childVS.state[0]
        childNode = childVS.state[1]
        # If the system is grid and we are connecting a node that was not in the existing grid,
        if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
            # Get internal cost
            internalCost = childVS.get(costGrid.GridInternalSystemNodalDiscountedCost)
            # Get half the length of all new connections to the node
            newConnections = childDataset.cycleConnections(childNode, is_existing=False)
            newConnectionLengthHalved = sum(x.weight for x in newConnections) / 2.
            # Get external cost
            externalCostPerMeter = childVS.get(costGrid.GridExternalSystemNodalDiscountedCostPerMeter)
            externalCost = externalCostPerMeter * newConnectionLengthHalved
            # Add internal and external cost
            self.value += internalCost + externalCost


class GridSystemTotalLevelizedCost(V):

    section = 'system (grid)'
    option = 'system total levelized cost'
    aliases = ['gr_sys_tot_lvlzd_cst', 'gr_tot_lev']
    dependencies = [
        GridSystemTotalDiscountedDemand,
        GridSystemTotalDiscountedCost,
    ]
    units = 'dollars per kilowatt-hour'

    def compute(self):
        if self.get(GridSystemTotalDiscountedDemand) == 0:
            return 0
        return self.get(GridSystemTotalDiscountedCost) / float(self.get(GridSystemTotalDiscountedDemand))


class GridSystemTotalInternalInitialCost(V):

    section = 'system (grid)'
    option = 'system total internal initial cost'
    aliases = ['gr_sys_tot_int_init_cst', 'gr_tot_iic']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # Get
        childDataset = childVS.state[0]
        childNode = childVS.state[1]
        # If the system is grid and we are connecting a node that was not in the existing grid,
        if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
            # Get internal cost
            internalCost = childVS.get(costGrid.GridInternalSystemInitialCost)
            # Add up internal cost
            self.value += internalCost


class GridSystemTotalInternalDiscountedRecurringCost(V):

    section = 'system (grid)'
    option = 'system total internal discounted recurring cost'
    aliases = ['gr_sys_tot_int_disc_rcrg_cst', 'gr_tot_idrc']
    default = 0
    units = 'dollars'

    def aggregate(self, childVS):
        # Get
        childDataset = childVS.state[0]
        childNode = childVS.state[1]
        # If the system is grid and we are connecting a node that was not in the existing grid,
        if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
            # Get internal cost
            internalAnnualCost = childVS.get(costGrid.GridInternalSystemRecurringCostPerYear)
            dcff = self.get(finance.DiscountedCashFlowFactor)
            # Apply cost factor and add up internal cost
            self.value += (dcff * internalAnnualCost)


class GridSystemTotalInitialCost(V):

    section = 'system (grid)'
    option = 'system total initial cost'
    aliases = ['gr_sys_tot_init_cst', 'gr_tot_init']
    dependencies = [
        GridSystemTotalInternalInitialCost,
        GridSystemTotalExternalInitialCost,
    ]
    units = 'dollars'

    def compute(self):
        return self.get(GridSystemTotalInternalInitialCost) + \
               self.get(GridSystemTotalExternalInitialCost)


class GridSystemTotalDiscountedRecurringCost(V):

    section = 'system (grid)'
    option = 'system total discounted recurring cost'
    aliases = ['gr_sys_tot_disc_rcrg_cst', 'gr_tot_drc']
    dependencies = [
        GridSystemTotalExternalDiscountedRecurringCost,
        GridSystemTotalInternalDiscountedRecurringCost,
    ]
    units = 'dollars'

    def compute(self):
        # Sum internal and external recurring costs and apply discounted cash flow factor
        intlCostPerYear = self.get(GridSystemTotalExternalDiscountedRecurringCost)
        extlCostPerYear = self.get(GridSystemTotalInternalDiscountedRecurringCost)
        return (intlCostPerYear + extlCostPerYear)


class GridSystemTotalExistingNetworkLength(V):

    section = 'system (grid)'
    option = 'system total existing network length'
    aliases = ['gr_sys_tot_ntwk_lgth', 'gr_tot_enl']
    units = 'meters'

    # Don't understand why we need this
    dependencies = [System]

    def compute(self):
        return self.state[0].sumNetworkWeight(is_existing=True)


class GridSystemTotalProposedNetworkLength(V):

    section = 'system (grid)'
    option = 'system total proposed network length'
    aliases = ['gr_sys_tot_prop_ntwk_lgth', 'gr_tot_pnl']
    units = 'meters'

    # Don't understand why we need this
    dependencies = [System]

    def compute(self):
        return self.state[0].sumNetworkWeight(is_existing=False)


# VariableStore

class VariableStore(VS):

    variableModules = [
        finance,
        demographics,
        demand,
        costDistribution,
        costOffGrid,
        costMiniGrid,
        costGrid,
    ]
    variableClasses = [
        Metric,
        System,
    ]
    aggregateClasses = [
        OffGridSystemTotal,
        OffGridSystemTotalDiscountedDemand,
        OffGridSystemTotalDiscountedCost,
        OffGridSystemTotalDiscountedDieselCost,
        OffGridSystemTotalInitialCost,
        OffGridSystemTotalDiscountedRecurringCost,
        OffGridSystemTotalDiscountedDieselFuelCost,
        MiniGridSystemTotal,
        MiniGridSystemTotalDiscountedDemand,
        MiniGridSystemTotalDiscountedCost,
        MiniGridSystemTotalInitialCost,
        MiniGridSystemTotalDiscountedRecurringCost,
        MiniGridSystemTotalDiscountedDieselFuelCost,
        GridSystemTotal,
        GridSystemTotalDiscountedDemand,
        GridSystemTotalDiscountedCost,
        GridSystemTotalInternalInitialCost,
        GridSystemTotalExternalInitialCost,
        GridSystemTotalInternalDiscountedRecurringCost,
        GridSystemTotalExternalDiscountedRecurringCost,
    ]
    summaryClasses = [
        OffGridSystemTotalLevelizedCost,
        MiniGridSystemTotalLevelizedCost,
        GridSystemTotalLevelizedCost,
        GridSystemTotalInitialCost,
        GridSystemTotalDiscountedRecurringCost,
        GridSystemTotalExistingNetworkLength,
        GridSystemTotalProposedNetworkLength,
    ]



# Set order

roots = [
    Metric, 
    OffGridSystemTotal,
    OffGridSystemTotalInitialCost,
    OffGridSystemTotalDiscountedDieselCost,
    OffGridSystemTotalDiscountedDieselFuelCost,
    OffGridSystemTotalDiscountedRecurringCost,
    OffGridSystemTotalLevelizedCost,
    MiniGridSystemTotal,
    MiniGridSystemTotalInitialCost,
    MiniGridSystemTotalDiscountedDieselFuelCost,
    MiniGridSystemTotalDiscountedRecurringCost,
    MiniGridSystemTotalLevelizedCost,
    GridSystemTotal,
    GridSystemTotalInitialCost,
    GridSystemTotalDiscountedRecurringCost,
    GridSystemTotalLevelizedCost,
    GridSystemTotalExistingNetworkLength,
    GridSystemTotalProposedNetworkLength,
]
sections = [
    'finance',
    'demographics',
    'demand',
    'demand (peak)',
    'demand (household)',
    'demand (productive)',
    'demand (social infrastructure)',
    'distribution',
    'system (off-grid)',
    'system (mini-grid)',
    'system (grid)',
    'metric',
]
