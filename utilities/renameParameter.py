#!/usr/bin/env python
import script_process
from np import model
from np.model import Session


configuration = script_process.connect()
for scenario in Session.query(model.Scenario):
    metricConfiguration = scenario.input['metric configuration']
    valueByName = metricConfiguration['demand (productive)']
    value = valueByName['productive unit demand']
    del valueByName['productive unit demand']
    valueByName['productive unit demand per household per year'] = value
    scenario.input = metricConfiguration
    scenario.status = model.statusNew
    scenario.commit()
