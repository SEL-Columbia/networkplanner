#!/usr/bin/env python
'Reset database'
# Import pylons modules
from pylons import config
# Import system modules
import os
import shutil
# Import custom modules
import script_process
from np import model
from np.model import Base, Session


# If we are running the command as a script,
if __name__ == '__main__':
    # Connect
    configuration = script_process.connect()
    config['storage_path'] = configuration.get('app:main', 'storage_path')
    storagePath = config['storage_path']
    storageBackupPath = storagePath + '_'
    if os.path.exists(storageBackupPath):
        shutil.rmtree(storageBackupPath)
    shutil.move(storagePath, storageBackupPath)
    # Create new database
    Base.metadata.bind = Session.bind
    Base.metadata.reflect()
    Base.metadata.drop_all()
    Base.metadata.create_all()
