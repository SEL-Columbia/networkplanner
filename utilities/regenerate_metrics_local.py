'Regenerate metrics local from dataset_store'
from pylons import config
import sys
import csv
import script_process
from np import model
from np.lib import dataset_store, store, metric, variable_store as VS
from np.model import Base, Session
from sqlalchemy import and_

def specialSaveMetricsCSV(ds, targetPath, metricModel, headerType=VS.HEADER_TYPE_SECTION_OPTION):
    'Save node-level metrics in CSV format'
    # Make sure that nodes exist
    if not ds.countNodes():
        return

    # Prepare column headers in order
    # Use the 1st node's input to get the "pass-through" fields 
    node = ds.cycleNodes().next()
    nodeInput = node.input
    headerPacks = [('', key) for key in sorted(nodeInput)]

    # get the section/option values in order from the model
    # and append to the headerPacks
    # Note:  metricModel.VariableStore.variableClasses should have all the
    #        the variableClasses associated with the model as long as 
    #        metricModel.VariableStore() has been called.
    baseVars = metricModel.VariableStore.variableClasses
    baseVarHeaders = [(var.section, var.option) for var in 
                      sorted(baseVars, key=lambda v: (v.section, v.option))]
    headerPacks.extend(baseVarHeaders)
    headerPacksToNames = VS.getFieldNamesForHeaderPacks(metricModel, 
                            headerPacks, headerType)
   
    csvWriter = csv.writer(open(store.replaceFileExtension(targetPath, 'csv'), 'wb'))
    csvWriter.writerow(['PROJ.4 ' + ds.getProj4()])

    csvWriter.writerow([headerPacksToNames[(section, option)] for 
                        section, option in headerPacks])

    # csvWriter.writerow(['%s > %s' % (section.capitalize(), option.capitalize()) if section else option.capitalize() for section, option in headerPacks])
    # For each node,
    for node in ds.cycleNodes():
        # Write row
        csvWriter.writerow([node.output.get(section, {}).get(option, '') if section else node.input.get(option, '') for section, option in headerPacks])


# If the user is running the script from the command-line,
if __name__ == '__main__':
    # Connect (get config and setup model from appropriate DB)
    configuration = script_process.connect()

    # get ids from stdin into a list
    ids = []
    for id in sys.stdin:
        ids.append(int(id))

    # required to know where scenarios dir is
    config['storage_path'] = configuration.get('app:main', 'storage_path')

       # Iterate through scenarios
    scenarios = Session.query(model.Scenario).\
            filter(and_(model.Scenario.id.in_(ids), 
                   (model.Scenario.status == model.statusDone))).\
            order_by(model.Scenario.id)

    for scenario in scenarios:
        scenarioFolder = scenario.getDatasetPath()
         
        datasetPath = store.replaceFileExtension(scenarioFolder, 'db')
        ds = dataset_store.load(datasetPath)
        metricModel = metric.getModel(scenario.input['metric model name'])
        vs = metricModel.VariableStore()
        specialSaveMetricsCSV(ds, "metrics-local-%s.csv" % scenario.id, metricModel)
        
