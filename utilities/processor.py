#!/usr/bin/env python
"""\
Cluster-side incoming consumer and outgoing producer

1. Get scenario from incoming queue
2. Process it 
3. Put result on outgoing queue

Po-Han "Freeza" Huang
Roy Hyunjin Han
"""
# Import pylons modules
from pylons import config
# Import system modules
from amqplib import client_0_8 as amqp
import cPickle as pickle
import traceback
import socket
import urllib
import shutil
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
    servicePort = int(configuration.get('server:main', 'port')) + 3
    localSocket = socket.socket()
    try:
        localSocket.bind(('', servicePort))
    except socket.error:
        # print 'Either another instance of %s is running or port %s is in use' % (__file__, port)
        sys.exit(1)
    # Ping central server
    urllib.urlopen(safe['web']['url'] + '/processors/update')
    # Load AMQP settings
    amqpHost, amqpUsername, amqpPassword = getValues('amqp', ['host', 'username', 'password'])
    incomingQueue, incomingExchange, incomingKey = getValues('amqp incoming', ['queue', 'exchange', 'key'])
    outgoingQueue, outgoingExchange, outgoingKey = getValues('amqp outgoing', ['queue', 'exchange', 'key'])
    # Connect to AMQP server
    connection = amqp.Connection(host=amqpHost, userid=amqpUsername, password=amqpPassword)
    channel = connection.channel()
    # Bind exchange to queue
    channel.queue_declare(queue=incomingQueue, durable=True, exclusive=False, auto_delete=False)
    channel.exchange_declare(exchange=incomingExchange, type='direct', durable=True, auto_delete=False)
    channel.queue_bind(queue=incomingQueue, exchange=incomingExchange, routing_key=incomingKey)
    # Loop
    while True:
        # Try to get the next incoming message
        incomingMessage = channel.basic_get(incomingQueue)
        # If a message does not exist,
        if not incomingMessage:
            # Take a break
            break
        # Unpack scenario from incoming message
        incomingPack = pickle.loads(incomingMessage.body)
        scenarioID, scenarioInput, scenarioData = incomingPack
        print 'Processing scenario %s' % scenarioID
        # Add scenario to local database
        scenario = model.Scenario(None, u'', model.scopePrivate)
        scenario.input = scenarioInput
        Session.add(scenario)
        Session.commit()
        # Unzip
        scenarioFolder = scenario.getFolder()
        store.unzipData(scenarioFolder, scenarioData)
        # Run
        try:
            scenario.run()
            scenario.status = model.statusDone
        except:
            scenario.output = dict(traceback=''.join(traceback.format_exception(*sys.exc_info())))
            scenario.status = model.statusFailed
        finally:
            Session.commit()
        # Pack result into outgoing message
        outgoingPack = scenarioID, scenario.output, open(scenarioFolder + '.zip', 'rb').read() if os.path.exists(scenarioFolder + '.zip') else None, scenario.status
        # Send outgoing message
        outgoingMessage = amqp.Message(pickle.dumps(outgoingPack))
        outgoingMessage.properties['delivery_mode'] = 2
        channel.basic_publish(outgoingMessage, exchange=outgoingExchange, routing_key=outgoingKey)
        # Delete incoming message
        channel.basic_ack(incomingMessage.delivery_tag)
        # Clean up
        shutil.rmtree(scenarioFolder)
        store.removeSafely(scenarioFolder + '.zip')
        Session.delete(scenario)
        Session.commit()
    # Close channel
    channel.close()
    # Close connection
    connection.close()
