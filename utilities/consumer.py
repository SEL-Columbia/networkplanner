#!/usr/bin/env python
"""\
Server-side incoming consumer

1. Get result from outgoing queue
2. Put result into database

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
# Import custom modules
import script_process
from np import model
from np.model import Session
from np.config import environment
from np.lib import store


def saveResult(outgoingMessage):
    'Save result in local database'
    # Unpack result from outgoing message
    outgoingPack = pickle.loads(outgoingMessage.body)
    scenarioID, scenarioOutput, scenarioData, scenarioStatus = outgoingPack
    print 'Consuming scenario %s' % scenarioID
    # Load scenario from local database
    scenario = Session.query(model.Scenario).get(scenarioID)
    # If the scenario does not exist,
    if not scenario:
        print 'Scenario %s does not exist' % scenarioID
        return
    # Get folder
    scenarioFolder = scenario.getFolder()
    # Save data
    if scenarioData:
        scenarioPath = scenarioFolder + '.zip'
        open(scenarioPath, 'wb').write(scenarioData)
        store.unzipData(scenarioFolder, scenarioData)
    # Delete outgoing message
    channel.basic_ack(outgoingMessage.delivery_tag)
    # Save output
    scenario.output = scenarioOutput
    scenario.status = scenarioStatus
    Session.commit()
    # Post to callback
    scenario.postCallback()


# If the script is running,
if __name__ == '__main__':
    # Connect
    configuration = script_process.connect()
    config['storage_path'] = configuration.get('app:main', 'storage_path')
    safe = environment.loadSafe(configuration.get('app:main', 'safe_path'))
    getValues = lambda section, options: [safe[section][x] for x in options]
    # Make sure that only a single instance is running
    servicePort = int(configuration.get('server:main', 'port')) + 4
    localSocket = socket.socket()
    try:
        localSocket.bind(('', servicePort))
    except socket.error:
        # print 'Either another instance of %s is running or port %s is in use' % (__file__, port)
        sys.exit(1)
    # Load AMQP settings
    amqpHost, amqpUsername, amqpPassword = getValues('amqp', ['host', 'username', 'password'])
    outgoingQueue, outgoingExchange, outgoingKey = getValues('amqp outgoing', ['queue', 'exchange', 'key'])
    # Connect to AMQP server
    connection = amqp.Connection(host=amqpHost, userid=amqpUsername, password=amqpPassword)
    channel = connection.channel()
    # Bind exchange to queue
    channel.queue_declare(queue=outgoingQueue, durable=True, exclusive=False, auto_delete=False)
    channel.exchange_declare(exchange=outgoingExchange, type='direct', durable=True, auto_delete=False)
    channel.queue_bind(queue=outgoingQueue, exchange=outgoingExchange, routing_key=outgoingKey)
    # Bind callback to queue
    channel.basic_consume(queue=outgoingQueue, callback=saveResult)
    # Wait for messages
    while True:
        channel.wait()
    # Close
    channel.close()
    connection.close()
