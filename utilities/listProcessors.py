#!/usr/bin/env python
'Requeue pending scenarios'
# Import custom modules
import script_process
from np import model
from np.model import Session


# If we are running the command as a script,
if __name__ == '__main__':
    # Connect
    script_process.connect()
    # List
    for processorIP, processorWhen in Session.query(model.Processor.ip, model.Processor.when_updated).order_by(model.Processor.when_updated):
        print '{}\t{}'.format(processorIP, processorWhen.strftime('%Y%m%d %H:%M'))
    # Commit
    Session.commit()
