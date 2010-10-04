#!/usr/bin/env python
"""\
Server-side incoming producer

1. Get scenario from database
3. Put scenario on incoming queue

Po-Han "Freeza" Huang
Roy Hyunjin Han
"""
# Import pylons modules
from pylons import config
# Import system modules
from amqplib import client_0_8 as amqp
import cPickle as pickle
import socket
import sys
import os
# Import custom modules
import script_process
from np import model
from np.model import Session
from np.config import environment
from np.lib import store


# If the script is running,
if __name__ == '__main__':
    # Connect
    configuration = script_process.connect()
    config['storage_path'] = configuration.get('app:main', 'storage_path')
    safe = environment.loadSafe(configuration.get('app:main', 'safe_path'))
    getValues = lambda section, options: [safe[section][x] for x in options]
    # Make sure that only a single instance is running
    servicePort = int(configuration.get('server:main', 'port')) + 2
    localSocket = socket.socket()
    try:
        localSocket.bind(('', servicePort))
    except socket.error:
        # print 'Either another instance of %s is running or port %s is in use' % (__file__, port)
        sys.exit(1)
    # Load AMQP settings
    amqpHost, amqpUsername, amqpPassword = getValues('amqp', ['host', 'username', 'password'])
    incomingQueue, incomingExchange, incomingKey = getValues('amqp incoming', ['queue', 'exchange', 'key'])
    # Connect to AMQP server
    connection = amqp.Connection(host=amqpHost, userid=amqpUsername, password=amqpPassword)
    channel = connection.channel()
    # For each new scenario,
    for scenario in Session.query(model.Scenario).filter(model.Scenario.status==model.statusNew):
        # Mark scenario as pending
        scenario.status = model.statusPending
        Session.commit()
        # Pack incoming message
        scenarioFolder = scenario.getFolder()
        scenarioPath = scenarioFolder + '.zip'
        if not os.path.exists(scenarioPath):
            store.zipFolder(scenarioPath, scenarioFolder)
        incomingPack = scenario.id, scenario.input, open(scenarioPath, 'rb').read()
        # Send incoming message
        incomingMessage = amqp.Message(pickle.dumps(incomingPack))
        incomingMessage.properties['delivery_mode'] = 2
        channel.basic_publish(incomingMessage, exchange=incomingExchange, routing_key=incomingKey)
    # Close channel
    channel.close()
    # Close connection
    connection.close()
