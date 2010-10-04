'Generate helper functions for data storage'
# Import system modules
import random
import os
import cPickle as pickle
import cStringIO as StringIO


# Expand

basePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def expandBasePath(relativePath):
    return os.path.join(basePath, relativePath)


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


# Folders

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
