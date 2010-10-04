'Make sure that we can load datasets properly'
# Import system modules
import unittest
import os
# Import custom modules
from np.lib import dataset_store


basePath = os.path.dirname(os.path.abspath(__file__))
dataPath = os.path.join(os.path.dirname(os.path.dirname(basePath)), 'public', 'files')
csvPath = os.path.join(dataPath, 'demographicsXY.csv')
zipPath = os.path.join(dataPath, 'demographics.zip')


class TestDatasetStore(unittest.TestCase):
    'Test dataset_store functions'

    def assertDigest(self, digest, datasetPath):
        # For each row,
        for attributeByName in digest(datasetPath)[1]:
            # Make sure that we have coordinates
            self.assertTrue('x' in attributeByName)
            self.assertTrue('y' in attributeByName)

    def test_digestNodesFromCSV(self):
        return self.assertDigest(dataset_store.digestNodesFromCSV, csvPath)

    def test_digestNodesFromZIP(self):
        return self.assertDigest(dataset_store.digestNodesFromZIP, zipPath)
