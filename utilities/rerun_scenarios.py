'Re Run Scenarios using input metrics and current model'
from pylons import config
import shutil
import sys
import os, errno
import script_process
from np import model
from np.model import Base, Session
from sqlalchemy import and_

def mkdir_p(path):
    """create directory only if it exists AND don't fail if it does"""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise


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
        # Backup existing scenario dir
        scenarioFolder = scenario.getFolder()
        scenarioBackupFolder = scenarioFolder.replace(storagePath, storageBackupPath)
        if not os.path.exists(scenarioBackupFolder):
            os.makedirs(scenarioBackupFolder)

        #Move everything EXCEPT the demographics file and input network
        demographicsFile = scenario.input['demographic file name']
        networkFile = ""
        if (scenario.input['network configuration']['network'].\
                has_key('existing networks')):
            networkFile = scenario.input['network configuration']['network']\
                    ['existing networks']

        moveFiles = [ os.path.join(scenarioFolder, f) for f in 
                os.listdir(scenarioFolder) if not 
                (f == demographicsFile or f == "network") ]

        for moveFile in moveFiles:
            newFile = moveFile.replace(storagePath, storageBackupPath)
            shutil.move(moveFile, newFile)

        #Copy demographics file and network file (just in case)
        fullDemographicsFile = os.path.join(scenarioFolder, demographicsFile)
        copyDemographicsFile = fullDemographicsFile.replace(storagePath, storageBackupPath)
        shutil.copy(fullDemographicsFile, copyDemographicsFile)
        if(networkFile):
            fullNetworkFile = os.path.join(scenarioFolder, networkFile)
            fullCopyNetworkFile = fullNetworkFile.replace(storagePath, storageBackupPath)
            copyNetworkDir, copyNetworkFile = os.path.split(fullCopyNetworkFile)
            mkdir_p(copyNetworkDir)
            shutil.copy(fullNetworkFile, copyNetworkFile)

        #run scenario
        print "running scenario id: %s" % scenario.id
        scenario.run()
