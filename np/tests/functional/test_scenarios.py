import os
import unittest
import json

# Import custom modules
from np.lib import dataset_store
from np.lib import metric
from np.lib import network


basePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
baseDirPath = os.path.dirname(os.path.dirname(basePath))
outputDataPath = os.path.join(baseDirPath, 'test_output')
inputDataPath = os.path.join(baseDirPath, 'test_data')

class TestScenarios(unittest.TestCase):
    'Test running a scenario'

    def test_scenarioRun(self):
        'for now, just make sure it runs'
        sourcePath = os.path.join(inputDataPath, "sample_demand_nodes.csv")
        # make output dir if not exists
        if not os.path.exists(outputDataPath):
            os.makedirs(outputDataPath)

        targetPath = os.path.join(outputDataPath, "dataset.db")
        datasetStore = dataset_store.create(targetPath, sourcePath)
        
        """
        // Sample Model Parameter JSON
        metricValueByOptionBySection = {
            'demand (household)': 
                {'household unit demand per household per year': 50}
        }
        """
        metricConfigPath = os.path.join(baseDirPath, "sample_metric_params.json")
        metricConfiguration = json.load(open(metricConfigPath, 'r'))

        """
        // Sample Model Parameter JSON
        networkValueByOptionBySection = {
            'algorithm': 
                {'minimum node count per subnetwork': 2}
        }
        """
        networkConfigPath = os.path.join(baseDirPath, "network_params.json")
        networkConfiguration = json.load(open(networkConfigPath, 'r'))

        # Run metric model
        metricModel = metric.getModel("mvMax5")
        metricValueByOptionBySection = datasetStore.applyMetric(metricModel, metricConfiguration)

        # Now that metrics (mvMax in particular) have been calculated
        # we can build the network
        networkModel = network.getModel("modKruskal")
        networkValueByOptionBySection = datasetStore.buildNetwork(networkModel, networkConfiguration)

        # Now that the network's been built (and the electrification option 
        # is chosen) run the aggregate calculations
        metricValueByOptionBySection = datasetStore.updateMetric(metricModel, metricValueByOptionBySection)

        metric.saveMetricsConfigurationCSV(os.path.join(outputDataPath, 'metrics-job-input'), metricConfiguration)
        metric.saveMetricsCSV(os.path.join(outputDataPath, 'metrics-global'), metricModel, metricValueByOptionBySection)
        datasetStore.saveMetricsCSV(os.path.join(outputDataPath, 'metrics-local'), metricModel)
        datasetStore.saveSegmentsSHP(os.path.join(outputDataPath, 'networks-proposed'), is_existing=False)

