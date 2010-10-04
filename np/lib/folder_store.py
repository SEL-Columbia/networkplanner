# Import system modules
import os
import re
import glob
# Import custom modules
import store


# Set constants
folderNames = 'demographics', 'metrics', 'networks'
# Set patterns
pattern_timestamp = re.compile('(\d+)-')
pattern_name = re.compile(r'[a-zA-Z1-9_\- (),.]+')


# Core

class Store(object):

    def __init__(self, basePath='.'):
        # Make the folder if it doesn't exist
        self.basePath = store.makeFolderSafely(basePath)
        # Set folderPathByName
        self.folderPathByName = dict((folderName, os.path.join(basePath, '%d-%s' % (folderIndex + 1, folderName))) for folderIndex, folderName in enumerate(folderNames))

    # Fill

    def fillPath(self, baseFolderName, folderName):
        'Returns a function that expands a fileName into a filePath'
        # Make sure that folderName is valid
        match = pattern_name.match(folderName)
        if not match: raise FolderError('Invalid name: %s\n%s' % (folderName, 'Names can have letters, digits, underscores, hyphens, spaces, parentheses, commas and periods.'))
        # Fill path
        baseFolderPath = store.makeFolderSafely(self.folderPathByName[baseFolderName])
        stampedFolderName = '%s-%s' % (store.makeTimestamp(), folderName)
        folderPath = store.makeFolderSafely(os.path.join(baseFolderPath, stampedFolderName))
        # Return
        return lambda fileName: os.path.join(folderPath, fileName)

    def fillDemographicPath(self, name):
        return self.fillPath('demographics', name)

    def fillMetricPath(self, name):
        return self.fillPath('metrics', name)

    def fillNetworkPath(self, name):
        return self.fillPath('networks', name)

    # Get paths

    def getPaths(self, baseFolderName, folderName):
        'Return a list of paths with the latest first'
        # Get paths
        baseFolderPath = self.folderPathByName[baseFolderName]
        folderPaths = glob.glob(os.path.join(baseFolderPath, '*-%s' % folderName))
        # Sort by timestamp
        folderPacks = [(pattern_timestamp.match(store.extractFileBaseName(x)).group(1), x) for x in folderPaths]
        folderPacks.sort()
        folderPaths = [x[1] for x in reversed(folderPacks)]
        # Append fileNames
        return folderPaths

    def getDemographicPaths(self, name): 
        return self.getPaths('demographics', name)

    def getMetricPaths(self, name): 
        return self.getPaths('metrics', name)

    def getNetworkPaths(self, name): 
        return self.getPaths('networks', name)

    # Get path

    def getDemographicPath(self, name): 
        return getPath(name, self.getDemographicPaths, 'demographic')

    def getMetricPath(self, name): 
        return getPath(name, self.getMetricPaths, 'metric')

    def getNetworkPath(self, name): 
        return getPath(name, self.getNetworkPath, 'network')

    # Get information

    def getMetricInformation(self, metricName):
        pass


# Derive



# Get

def getFolderName(filePath):
    return os.path.basename(os.path.dirname(filePath))

def getPath(name, method, description):
    paths = method(name)
    if not paths: raise FolderError('Could not find %s: %s' % (description, name))
    return paths[0]


# Error

class FolderError(Exception):
    pass
