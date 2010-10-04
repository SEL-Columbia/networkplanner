#!/usr/bin/env python
'Migrate database'
# Import pylons modules
from pylons import config
# Import system modules
import cPickle as pickle
import datetime
import sqlite3
import shutil
import os
# Import custom modules
import script_process
from np import model
from np.model import Base, Session
from np.lib import store


# If the user is running the script from the command-line,
if __name__ == '__main__':
    # Connect
    configuration = script_process.connect()
    config['storage_path'] = configuration.get('app:main', 'storage_path')
    storagePath = config['storage_path']
    storageBackupPath = storagePath + '_'
    # if os.path.exists(storageBackupPath):
        # shutil.rmtree(storageBackupPath)
    shutil.move(storagePath, storageBackupPath)
    # Backup old database
    # databasePath = configuration.get('app:main', 'sqlalchemy.url').replace('sqlite:///', '')
    # databaseBackupPath = databasePath + '_'
    # if os.path.exists(databaseBackupPath):
        # shutil.rmtree(databaseBackupPath)
    # shutil.move(databasePath, databaseBackupPath)
    connection = sqlite3.connect('production.db')
    cursor = connection.cursor()
    # Create new database
    Base.metadata.bind = Session.bind
    Base.metadata.reflect()
    Base.metadata.drop_all()
    Base.metadata.create_all()
    # Migrate people
    cursor.execute('SELECT username, password_hash, nickname, email, email_sms, minutes_offset, rejection_count, pickled FROM people')
    for username, password_hash, nickname, email, email_sms, minutes_offset, rejection_count, pickled in cursor.fetchall():
        person = model.Person(username, password_hash, nickname, email, email_sms)
        person.minutes_offset = minutes_offset
        person.rejection_count = rejection_count
        person.pickled = pickled
        Session.add(person)
        Session.commit()
    personByUsername = dict((x.username, x) for x in Session.query(model.Person))
    # Migrate scenarios
    cursor.execute('SELECT scenarios.id, username, name, scope, when_created, input FROM scenarios INNER JOIN people ON scenarios.owner_id=people.id WHERE status=?', [model.statusDone])
    for scenarioID, username, name, scope, when_created, input in cursor.fetchall():
        scenario = model.Scenario(personByUsername[username].id, name, scope)
        scenario.when_created = datetime.datetime.strptime(when_created, '%Y-%m-%d %H:%M:%S.%f')
        scenarioInput = pickle.loads(str(input))

        existingNetworkPath = scenarioInput['network configuration']['network']['existing network path']
        del scenarioInput['network configuration']['network']['existing network path']
        if existingNetworkPath:
            scenarioInput['network configuration']['network']['existing networks'] = u'network/network/existing networks.zip'

        scenario.input = scenarioInput
        Session.add(scenario)
        Session.commit()
        shutil.copytree(store.binPath(os.path.join(storageBackupPath, 'scenarios'), scenarioID), store.binPath(os.path.join(storagePath, 'scenarios'), scenario.id))
