#!/usr/bin/env python
'Requeue pending scenarios'
# Import custom modules
import script_process
from np import model
from np.model import Session


# If we are running the command as a script,
if __name__ == '__main__':
    # Connect
    configuration = script_process.connect()
    # Requeue
    Session.execute(model.scenarios_table.update().where(model.scenarios_table.c.status==model.statusPending).values(status=model.statusNew))
    # Commit
    Session.commit()
