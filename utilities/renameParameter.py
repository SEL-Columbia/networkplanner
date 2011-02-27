#!/usr/bin/env python
# Import pylons modules
from pylons import config
# Import system modules
import glob
import os
# Import custom modules
import script_process
from np import model
from np.model import Session


# Connect
configuration = script_process.connect()
config['storage_path'] = configuration.get('app:main', 'storage_path')
# For each scenario,
for scenario in Session.query(model.Scenario).order_by(model.Scenario.id):
    print scenario.getFolder(),
    scenarioInput = scenario.input
    scenario.input = None
    Session.commit()
    try:
        metricConfiguration = scenarioInput['metric configuration']
        valueByName = metricConfiguration['demand (productive)']
        try:
            value = valueByName['productive unit demand']
            del valueByName['productive unit demand']
            valueByName['productive unit demand per household per year'] = value
            scenario.input = scenarioInput
            print 'Changed parameter name'
        except KeyError:
            scenarioInput['demographic file name'] = os.path.basename(glob.glob(os.path.join(scenario.getFolder(), 'demographics.*'))[0])
            scenario.input = scenarioInput
            print 'Fixed demographic file name'
    except KeyError:
        metricConfiguration = scenarioInput
        scenarioInput = {
            'host url': 'http://october.mech.columbia.edu',
            'metric configuration': metricConfiguration,
            'callback url': None,
            'metric model name': u'mvMax3',
            'network configuration': {
                'algorithm': {
                    'minimum node count per subnetwork': u'2'
                }, 
                'network': {
                    'existing networks': u'network/network/existing networks.zip' if os.path.exists(os.path.join(scenario.getFolder(), 'network')) else u''
                }
            },
            'network model name': u'modKruskal',
            'demographic file name': u'demographics.csv' if os.path.exists(os.path.join(scenario.getFolder(), 'demographics.csv')) else u'demographics.zip',
        }
        scenario.input = scenarioInput
        print 'Restored input'
    scenario.status = model.statusNew
    # Commit
    Session.commit()
