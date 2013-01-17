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
import signal
# Import custom modules
import script_process
from np import model
from np.model import Session, Job
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
    
    # Setup a signal handler to exit gracefully upon interrupt
    # If called during processing of a scenario, that scenario 
    # will be put into a Failed state
    def interrupt_handler(signum, frame):
        sys.exit(1)
    signal.signal(signal.SIGINT, interrupt_handler)

    # Prepare
    config['storage_path'] = configuration.get('app:main', 'storage_path')
    safe = environment.loadSafe(configuration.get('app:main', 'safe_path'))
    # Ping central server
    urllib.urlopen(safe['web']['url'] + '/processors/update')
    # For each new scenario,
    for scenario in Session.query(model.Scenario).filter(model.Scenario.status==model.statusNew):
        # Start log entry for this scenario
        Job.log("Start Scenario id %s" % scenario.id)
        # Mark scenario as pending
        scenario.status = model.statusPending
        Session.commit()
        try:
            # Run
            scenario.run()
            scenario.status = model.statusDone
            Job.log("End Scenario id %s" % scenario.id)
        except SystemExit:
            # Store traceback
            scenario.output = dict(traceback=''.join(traceback.format_exception(*sys.exc_info())))
            scenario.status = model.statusFailed
            Job.log("Kill Scenario id %s" % scenario.id)
            break
        except:
            # Store traceback
            scenario.output = dict(traceback=''.join(traceback.format_exception(*sys.exc_info())))
            scenario.status = model.statusFailed
            Job.log("Error Scenario id %s" % scenario.id)
        finally:
            # Commit here in case our process dies
            Session.commit()
            # Post to callback
            scenario.postCallback()

    Job.end()
    Session.commit() 
