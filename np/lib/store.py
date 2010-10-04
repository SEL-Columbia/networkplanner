'Generate helper functions for data storage'
# Import system modules
import re
import os
import sys
import math
import time
import random
import zipfile
import datetime
import itertools
import collections
import ConfigParser
import cPickle as pickle
import cStringIO as StringIO


# File

basePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def expandBasePath(relativePath):
    return os.path.join(basePath, relativePath)

def makeFolderSafely(folderPath):
    'Make a directory at the given folderPath' 
    # For each parentPath, 
    for parentPath in reversed(traceParentPaths(os.path.abspath(folderPath))): 
        # If the parentPath folder does not exist, 
        if not os.path.exists(parentPath): 
            # Make the parentPath folder 
            os.mkdir(parentPath) 
    # Return 
    return folderPath 
 
def traceParentPaths(folderPath): 
    'Return a list of parentPaths containing the given folderPath' 
    parentPaths = [] 
    parentPath = folderPath 
    while parentPath not in parentPaths: 
        parentPaths.append(parentPath) 
        parentPath = os.path.dirname(parentPath) 
    return parentPaths 

def removeSafely(filePath):
    if os.path.exists(filePath): 
        os.remove(filePath)

def binPath(rootPath, fileID):
    # Convert to an integer
    fileID = int(fileID)
    # Get the bin number
    binID = fileID / 31993 # Maximum number of subfolders in ext3 is 31998 but allow for 5 extra files
    # Return path
    return os.path.join(makeFolderSafely(os.path.join(rootPath, str(binID))), str(fileID))

def replaceFileExtension(filePath, newExtension):
    if not newExtension.startswith('.'): newExtension = '.' + newExtension
    base = os.path.splitext(filePath)[0]
    return base + newExtension

def extractFileBaseName(filePath):
    filename = os.path.split(filePath)[1]
    return os.path.splitext(filename)[0]

def verifyPath(filePath):
    if filePath and not os.path.exists(filePath): 
        raise StoreError('Path not found: %s' % filePath)
    return filePath

def fillPath(rootPath, relativeFolderPath, relativeFilePath):
    folderPath = os.path.join(rootPath, relativeFolderPath)
    filePath = os.path.join(folderPath, relativeFilePath)
    return os.path.abspath(filePath)



# Random

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'

def makeRandomString(length):
    'Generate a random string'
    return ''.join(random.choice(letters + numbers) for x in xrange(length))

def makeRandomAlphaNumericString(length):
    'Generate a random string containing at least one alphabet character and digit'
    # Generate candidates
    candidates = []
    candidates.append(random.choice(letters))
    candidates.append(random.choice(numbers))
    if length > 2:
        candidates.extend(random.choice(letters + numbers) for x in xrange(length - 2))
    random.shuffle(candidates)
    return ''.join(candidates[:length])

def makeRandomUniqueTicket(length, query):
    'Generate a random unique ticket given an SQLAlchemy mapped class'
    # Initialize
    numberOfPossibilities = len(letters + numbers) ** length
    iterationCount = 0
    # Loop through possibilities until our randomID is unique
    while iterationCount < numberOfPossibilities:
        # Make randomID
        iterationCount += 1
        randomID = makeRandomString(length)
        # If our randomID is unique, return it
        if not query.filter_by(ticket=randomID).first(): 
            return randomID


# Reduce

def reduceSets(packs, itemName):
    if not packs:
        return set()
    items = [x[itemName] for x in packs]
    return reduce(lambda x, y: x.union(y), items)


# Pickle

def setPickle(x):
    return pickle.dumps(x, protocol=2)

def getPickle(pickled_x):
    return pickle.load(StringIO.StringIO(pickled_x))


# Information

def saveInformation(filePath, valueByOptionBySection, fileExtension='info'):
    # Initialize
    configuration = ConfigParser.RawConfigParser()
    # For each section,
    for section in valueByOptionBySection:
        # Initialize
        valueByOption = valueByOptionBySection[section]
        # Add section
        addConfigurationSection(configuration, section, valueByOption)
    # Write
    filePath = replaceFileExtension(filePath, fileExtension)
    configuration.write(open(filePath, 'wt'))

def addConfigurationSection(configuration, section, valueByOption):
    # Add section
    configuration.add_section(section)
    # For each option,
    for option in valueByOption:
        # Initialize
        value = valueByOption[option]
        # If value is a dictionary,
        if isinstance(value, dict):
            # Add section
            sectionName = '%s.%s' % (section, option)
            addConfigurationSection(configuration, sectionName, value)
        # Otherwise
        else:
            # Add option
            configuration.set(section, option, value)

def loadInformation(filePath, fileExtension='info', convertByName=None):
    # Initialize
    configuration = ConfigParser.RawConfigParser()
    valueByOptionBySection = {}
    # Read
    filePath = replaceFileExtension(filePath, fileExtension)
    configuration.read(filePath)
    # For each section,
    for section in configuration.sections():
        # Initialize
        valueByOption = {}
        # For each option,
        for option in configuration.options(section):
            # Get value
            value = configuration.get(section, option)
            # Set option
            valueByOption[option] = convertByName[option](value) if convertByName else value
        # Store
        valueByOptionBySection[section] = valueByOption
    # Return
    return valueByOptionBySection

def loadQueue(queuePath, convertByName=None):
    # Load
    valueByNameBySection = loadInformation(queuePath, 'queue', convertByName)
    sections = valueByNameBySection.keys()
    # Set globalParameterByName
    globalParameterByName = valueByNameBySection.get('parameters', {})
    if 'parameters' in sections: 
        sections.remove('parameters')
    # Set parameterByTaskByName
    parameterByTaskByName = {}
    for section in sections:
        # Load
        valueByName = globalParameterByName.copy()
        valueByName.update(valueByNameBySection[section])
        # Save
        parameterByTaskByName[section] = valueByName
    # Return
    return parameterByTaskByName


# Model

def getModel(scriptPath, modelName, availableNames):
    # If the modelName is invalid,
    if modelName not in availableNames:
        raise StoreError('Model %s is not available' % modelName)
    # Load model
    modelFolderPath = os.path.dirname(scriptPath)
    sys.path.append(modelFolderPath)
    model = __import__(modelName)
    sys.path.remove(modelFolderPath)
    # Return
    return model


# Stringify

def stringifyList(items):
    return '\n' + '\n'.join(str(x) for x in items)

def stringifyNestedList(lists):
    return '\n' + '\n'.join(' '.join(str(item) for item in list) for list in lists)

def flattenList(items):
    return ' '.join(str(x) for x in items)

def flattenNestedList(lists):
    return '; '.join(' '.join(str(item) for item in list) for list in lists)

def flattenCoordinatesList(lists):
    return flattenNestedList(itertools.izip(lists[0], lists[1]))

def flattenDictionary(dictionary):
    return flattenNestedList(dictionary.iteritems())


# Unstringify

pattern_separator = re.compile(r'[\n;]')

def unstringifyStringList(content):
    lines = tuple(x.strip() for x in pattern_separator.split(content))
    return filter(lambda line: True if line else False, lines)

def unstringifyFloatList(content):
    return map(float, content.split())

def unstringifyDescendingFloatList(content):
    return sorted(unstringifyFloatList(content), reverse=True)

def unstringifyIntegerList(content):
    return map(int, content.split())

def unstringifyNestedList(content, parseItem):
    return tuple(tuple(parseItem(x) for x in line.split()) for line in unstringifyStringList(content))

def unstringifyNestedIntegerList(content):
    return unstringifyNestedList(content, int)

def unstringifyNestedFloatList(content):
    return unstringifyNestedList(content, float)

def unstringifyCoordinatesList(content):
    points = unstringifyNestedFloatList(content)
    xs = tuple(x for x, y in points)
    ys = tuple(y for x, y in points)
    return xs, ys

def unstringifyIntegerDictionary(content):
    return dict(unstringifyNestedIntegerList(content))

def unstringifyFloatDictionary(content):
    return dict(unstringifyNestedFloatList(content))


# Time

def recordElapsedTime(function):
    # Define wrapper
    def wrapper(*args, **kwargs):
        # Run
        startTimeInSeconds = time.time()
        resultByName = function(*args, **kwargs)
        endTimeInSeconds = time.time()
        # Record
        elapsedTimeInSeconds = int(round(endTimeInSeconds - startTimeInSeconds))
        if not resultByName: 
            resultByName = {}
        resultByName['elapsed time in seconds'] = elapsedTimeInSeconds
        print 'elapsed time in seconds = %s' % elapsedTimeInSeconds
        # Return
        return resultByName
    # Return
    return wrapper

def makeTimestamp(): 
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S') 


# Compress

def zipFolder(targetPath, sourceFolderPath, excludes=None):
    # Initialize
    if not excludes:
        excludes = []
    # Open zipFile
    zipFile = zipfile.ZipFile(targetPath, 'w', zipfile.ZIP_DEFLATED)
    # Walk sourceFolderPath
    for rootPath, directories, fileNames in os.walk(sourceFolderPath):
        # For each file,
        for fileName in set(fileNames).difference(excludes):
            filePath = os.path.join(rootPath, fileName)
            relativePath = filePath[len(sourceFolderPath) + 1:]
            zipFile.write(filePath, relativePath, zipfile.ZIP_DEFLATED)
    # Close zipFile
    zipFile.close()

def unzip(sourcePath, mainExtension, overwrite=False):
    'Unzip the sourcePath and return the file path with the given extension'
    # Make sure mainExtension starts with a period
    if not mainExtension.startswith('.'):
        mainExtension = '.' + mainExtension
    # Prepare
    sourceZip = zipfile.ZipFile(sourcePath)
    destinationPath = os.path.join(os.path.dirname(sourcePath), extractFileBaseName(sourcePath))
    mainFileName = ''
    # If the archive has not been unpacked yet or the user wants to overwrite,
    if not os.path.exists(destinationPath) or overwrite:
        makeFolderSafely(destinationPath)
        for name in sourceZip.namelist():
            if os.path.splitext(name)[1] == mainExtension:
                mainFileName = name
            sourceZip.extract(name, destinationPath)
        sourceZip.close()
    # If the archive has already been unpacked,
    else:
        for root, folders, files in os.walk(destinationPath):
            for f in files:
                if os.path.splitext(f)[1] == mainExtension:
                    mainFileName = f
                    break
    # If we found a file with a matching extension,
    if mainFileName:
        return 1, os.path.join(destinationPath, mainFileName)
    else:
        return 0, destinationPath

def unzipData(targetFolder, sourceData):
    'Unzip sourceData'
    # Prepare
    sourceZip = zipfile.ZipFile(StringIO.StringIO(sourceData))
    makeFolderSafely(targetFolder)
    # For each compressed file,
    for name in sourceZip.namelist():
        sourceZip.extract(name, targetFolder)
    # Close
    sourceZip.close()


# Validate

def assertPositive(x):
    assert x > 0, 'must be positive'

def assertNonNegative(x):
    assert x >= 0, 'must be non-negative'

def assertLessThanOne(x):
    assert x < 1, 'must be less than one'


# Warn

warningsByID = collections.defaultdict(list)

def pushWarning(referenceID, text):
    'Append text to the list for the corresponding referenceID'
    warningsByID[referenceID].append(text)

def popWarnings(referenceID):
    'Unload warnings for the given referenceID from memory'
    if referenceID not in warningsByID:
        return []
    texts = warningsByID[referenceID]
    del warningsByID[referenceID]
    return texts


# Parse

def parseCeilInteger(x):
    return int(math.ceil(float(x)))


# Split

def splitList(items, partCount):
    'Split list into similarly sized parts'
    # Initialize
    partLength = int(len(items) / partCount)
    sortedItems = sorted(items)
    listParts = []
    # For each part,
    for partIndex in xrange(partCount):
        indexS = partLength * partIndex
        indexE = indexS + partLength
        listPart = sortedItems[indexS : indexE]
        listParts.append(listPart)
    # Return
    return listParts


# Error

class StoreError(Exception):
    pass
