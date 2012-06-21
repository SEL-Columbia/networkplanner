"""
Regenerate the demographics file for a list of scenarios
Note that this only runs for scenarios in the "done" state
"""

from pylons import config
import shutil
import sys
import os
import script_process
from np import model
from np.model import Base, Session
from sqlalchemy import and_
from np.lib import store, dataset_store, geometry_store

def regenerate_demographic_file(scenario, proj4=geometry_store.proj4LL):
    """ In case demographic input file is lost, this regenerates it
    NOTE:  This uses the node dict stored in scenario.output.  
           The nodes there are all nodes from the original datasetStore
           Which may contain some "FAKE" nodes if the scenario had an
           input network.  
    """
    scenarioFolder = scenario.getFolder()
    store.makeFolderSafely(scenarioFolder)

    expandPath = lambda x: os.path.join(scenarioFolder, x)

    # recreate datasetStore
    targetPath = scenario.getDatasetPath()
    targetPath = targetPath.replace(".", "_tmp.") #Don't overwrite existing store if it's there
    datasetStore = dataset_store.Store(targetPath, proj4)
    nodeDict = scenario.output['variables']['node']
    datasetStore.addNodesFromNodeDict(nodeDict)

    sourcePath = expandPath(scenario.input['demographic file name'])
    datasetStore.saveNodesCSV(sourcePath)
    
    #delete the tmp dataset store
    os.remove(targetPath)


# If the user is running the script from the command-line,
if __name__ == '__main__':
    # Connect (get config and setup model from appropriate DB)
    configuration = script_process.connect()

    # get ids from stdin into a list
    ids = []
    for id in sys.stdin:
        ids.append(int(id))

    config['storage_path'] = configuration.get('app:main', 'storage_path')
    storagePath = config['storage_path']
    
    # create backup dir for any files we're overwriting for a scenario
    storageBackupPath = storagePath + '_bak'

    # Iterate through scenarios
    scenarios = Session.query(model.Scenario).\
            filter(and_(model.Scenario.id.in_(ids), 
                   (model.Scenario.status == model.statusDone))).\
            order_by(model.Scenario.id)

    for scenario in scenarios:
        # Backup existing demographics file
        scenarioFolder = scenario.getFolder()
        scenarioBackupFolder = scenarioFolder.replace(storagePath, storageBackupPath)
        if not os.path.exists(scenarioBackupFolder):
            os.makedirs(scenarioBackupFolder)

        demographicsFile = scenario.input['demographic file name']
        fullDemographicsFile = os.path.join(scenarioFolder, demographicsFile)
        if os.path.exists(fullDemographicsFile):
            copyDemographicsFile = fullDemographicsFile.replace(storagePath, storageBackupPath)
            shutil.copy(fullDemographicsFile, copyDemographicsFile)

        #run scenario
        print "regenerating demographics for scenario id: %s" % scenario.id
        regenerate_demographic_file(scenario)
