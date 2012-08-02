"""
Save input metrics file for all scenarios in a list
Note that this only runs for scenarios in the "done" state
"""

from pylons import config
import sys, os
import script_process
from np import model
from np.model import Session
from sqlalchemy import and_
from np.lib import store, metric

def save_job_input_file(scenario):
    """ Save scenario leve inputs """
    scenarioFolder = scenario.getFolder()
    store.makeFolderSafely(scenarioFolder)

    expandPath = lambda x: os.path.join(scenarioFolder, x)

    metricConfiguration = scenario.input['metric configuration'] 
    metric.saveMetricsConfigurationCSV(expandPath('metrics-job-input'), metricConfiguration)

    store.zipFolder(scenarioFolder + '.zip', scenarioFolder)


# If the user is running the script from the command-line,
if __name__ == '__main__':
    # Connect (get config and setup model from appropriate DB)
    configuration = script_process.connect()
    config['storage_path'] = configuration.get('app:main', 'storage_path')

    # get ids from stdin into a list
    ids = sys.stdin.readlines()

    # Iterate through scenarios saving input files
    scenarios = Session.query(model.Scenario).\
            filter(and_(model.Scenario.id.in_(ids), 
                   (model.Scenario.status == model.statusDone))).\
            order_by(model.Scenario.id)

    for scenario in scenarios:
        print "saving metric inputs for scenario id: %s" % scenario.id
        save_job_input_file(scenario)
