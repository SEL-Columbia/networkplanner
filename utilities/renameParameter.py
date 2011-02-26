#!/usr/bin/env python
# Import pylons modules
from pylons import config
# Import system modules
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
    try:
        metricConfiguration = scenarioInput['metric configuration']
        valueByName = metricConfiguration['demand (productive)']
        try:
            value = valueByName['productive unit demand']
            del valueByName['productive unit demand']
            valueByName['productive unit demand per household per year'] = value
            scenario.input = scenarioInput
            print 'Change parameter name'
        except KeyError:
            print 'Do nothing'
    except KeyError:
        metricConfiguration = scenarioInput
        scenario.input = {
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
            'demographic file name': u'demographics.csv' if os.path.exists(os.path.join(scenario.getFolder(), 'demographic.csv')) else u'demographics.zip',
        }
        print 'Restore input'
    scenario.status = model.statusNew
    # Commit
    Session.commit()
