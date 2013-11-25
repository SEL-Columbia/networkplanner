'Framework for computing metrics using different mathematical models'
# Import system modules
import csv
import copy
import itertools
# Import custom modules
from np.lib import store
from np import util


# Define model wrappers

def getModelNames():
    return ['mvMax5', 'mvMax4', 'mvMax3', 'mvMax2']

def getModel(modelName):
    return store.getModel(__file__, modelName, getModelNames())


# Define helpers

def computeSystemCounts(desiredCapacity, availableCapacities):
    'Return an array of system counts to approximate the desired capacity'
    # Sort availableCapacities from largest to smallest
    availableCapacities.sort(reverse=True)
    # Initialize
    capacityCounts = []
    remainingCapacity = desiredCapacity
    # For each availableCapacity,
    for availableCapacity in availableCapacities:
        # Divide remainingCapacity by availableCapacity
        availableCapacityCount = int(remainingCapacity / availableCapacity)
        capacityCounts.append(availableCapacityCount)
        # Compute remainingCapacity
        remainingCapacity = remainingCapacity % availableCapacity
    # If we have a remainder,
    if remainingCapacity:
        # Increment the smallest capacity
        capacityCounts[-1] += 1
    # Return
    return capacityCounts

def saveMetricsCSV(targetPath, metricModel, valueByOptionBySection):
    'Save scenario-level metrics as a CSV file'
    # Initialize
    csvFile = open(store.replaceFileExtension(targetPath, 'csv'), 'wt')
    csvWriter = csv.writer(csvFile)
    vs = metricModel.VariableStore
    for variableClass in sorted(itertools.chain(vs.aggregateClasses, 
                                                vs.summaryClasses), 
                                key=lambda x: (x.__module__, x.__name__)):
        section = variableClass.section
        option = variableClass.option
        value = valueByOptionBySection[section][option]
        csvWriter.writerow([section, option, value])
    csvFile.close()

def saveMetricsConfigurationCSV(targetPath, valueByOptionBySection):
    'Save scenario-level INPUT metrics as a CSV file'
    csvFile = open(store.replaceFileExtension(targetPath, 'csv'), 'wt')
    csvWriter = csv.writer(csvFile)
    # Note, this assumes section, option, value tuples returned by flatten function
    for section, option, value in sorted(util.flatten_to_tuples(valueByOptionBySection)):
        csvWriter.writerow([section, option, value])

    csvFile.close()
    
def saveMetricsConfigurationFullCSV(targetPath, metricModel, valueByOptionBySection):
    'Save scenario-level INPUT metrics WITH DETAIL as a CSV file'
    variableStore = metricModel.VariableStore(valueByOptionBySection)
    csvFile = open(store.replaceFileExtension(targetPath, 'csv'), 'wt')
    csvWriter = csv.writer(csvFile)
    # Note, this assumes section, option, value tuples returned by flatten function
    for section, option, value in sorted(util.flatten_to_tuples(valueByOptionBySection)):

        find_var = lambda x, section=section, option=option: \
                isinstance(x, type) and x.section == section and x.option == option
        var = filter(find_var, variableStore.variableClasses)[0]
        alias = ""
        if var.aliases and len(var.aliases) > 0:
            alias = var.aliases[0]
        csvWriter.writerow([section, option, alias, value, var.units, var.__doc__])

    csvFile.close()
