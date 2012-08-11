'Update the scenario input dict with a dict passed in at cmd line'
from pylons import config
import shutil
import sys
import os, errno
import script_process
from np import model
from np.model import Base, Session
from np import util
from sqlalchemy import and_


# If the user is running the script from the command-line,
if __name__ == '__main__':
    # Connect (get config and setup model from appropriate DB)
    configuration = script_process.connect()

    new_input = {}
    if(len(sys.argv) > 3):
        try:
            new_input = eval(sys.argv[3])
        except Exception as e:
            print("Error evaluating input dict: %s" % e)
            sys.exit(-1)
    else:
        print("required params:  -c <environment>.ini \"<input_dict_as_python>\"")
        sys.exit(-1)

    # get ids from stdin into a list
    ids = []
    for id in sys.stdin:
        ids.append(int(id))

    config['storage_path'] = configuration.get('app:main', 'storage_path')
    storagePath = config['storage_path']

    # Iterate through scenarios
    scenarios = Session.query(model.Scenario).\
            filter(model.Scenario.id.in_(ids)).\
            order_by(model.Scenario.id)

    for scenario in scenarios:

        #update the input and commit it
        scenInput = scenario.input
        scenario.input = None
        Session.commit()
        util.update(scenInput, new_input)
        scenario.input = scenInput
        Session.commit()
        print("updated input of scenario id: %s" % scenario.id)
