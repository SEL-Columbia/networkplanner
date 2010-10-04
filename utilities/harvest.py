#!/usr/bin/env python
'Harvest scenarios in queue'
# Import pylons modules
from pylons import config
# Import system modules
import sys
import cjson
import socket
import urllib
import traceback
# Import custom modules
import script_process
from np import model
from np.model import Session
from np.config import environment


# If we are running the command as a script,
if __name__ == '__main__':
    # Connect
    configuration = script_process.connect()
    # Ensure that only one instance of this script is running
    servicePort = int(configuration.get('server:main', 'port')) + 1
    localSocket = socket.socket()
    try:
        localSocket.bind(('', servicePort))
    except socket.error:
        sys.exit(1)
    # Prepare
    config['storage_path'] = configuration.get('app:main', 'storage_path')
    safe = environment.loadSafe(configuration.get('app:main', 'safe_path'))
    # Ping central server
    urllib.urlopen(safe['web']['url'] + '/processors/update')
    # For each new scenario,
    for scenario in Session.query(model.Scenario).filter(model.Scenario.status==model.statusNew):
        # Mark scenario as pending
        scenario.status = model.statusPending
        Session.commit()
        try:
            # Run
            scenario.run()
            scenario.status = model.statusDone
        except:
            # Store traceback
            scenario.output = dict(traceback=''.join(traceback.format_exception(*sys.exc_info())))
            scenario.status = model.statusFailed
        finally:
            # Commit here in case our process dies
            Session.commit()
            # Post to callback
            scenario.postCallback()
