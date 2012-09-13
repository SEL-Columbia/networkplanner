# Import system modules
import unittest
# Import custom modules
from np.lib import dataset_store as ds
from np.lib import network
from np.lib.network import modKruskal 

n1 = ds.Node((0,0), (0,0), {})
n1.metric = 1
n1.id = 1
n2 = ds.Node((1,0), (1,0), {})
n2.metric = 4
n2.id = 2
n3 = ds.Node((0,2), (0,2), {})
n3.metric = 2
n3.id = 3
n4 = ds.Node((3,0), (3,0), {})
n4.metric = 1
n4.id = 4
n5 = ds.Node((4,0), (4,0), {})
n5.metric = 1
n5.id = 5
n6 = ds.Node((3,2), (3,2), {})
n6.metric = 1
n6.id = 6

proj4 = '+proj=utm +zone=28 +ellps=WGS84 +datum=WGS84 +units=m +no_defs'

class TestModKruskal(unittest.TestCase):

    def setUp(self):
        # Initialize
        self.modKruskalVS = modKruskal.VariableStore()

    def testCreatingTwoSubnetsWithVaryingMetrics(self):
        'Broad test of modKruskal.buildNetworkFromNodes'
        nodes = [n1, n2, n3, n4, n5, n6]
        net = self.modKruskalVS.buildNetworkFromNodes(nodes, proj4)
        assert net.countSubnets() == 2
        assert net.countSegments() == 3
        # ensure that the 2 subnets contain appropriate nodes
        nodesPerSubnet = [list(subnet.cycleNodes()) for subnet in \
                net.cycleSubnets()]
        nodeIdsPerSubnet = [set([node.getID() for node in subnetNodes]) \
                for subnetNodes in nodesPerSubnet]
        # nodes 1, 2, 3 should be in one subnet
        assert set([1, 2, 3]) in nodeIdsPerSubnet
        # nodes 4, 5 should be in another subnet
        assert set([4, 5]) in nodeIdsPerSubnet
        # node 6 should NOT be in a subnet
        assert set([6]) not in nodeIdsPerSubnet
