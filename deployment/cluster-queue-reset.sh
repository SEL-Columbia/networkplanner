#!/bin/env bash
if [ ! -f .production.cfg ]; then
    echo "Please run this script in a directory containing .production.cfg"
fi
# If rabbitMQ has been reset,
if [ "`/usr/sbin/rabbitmqctl list_users|grep guest`" = "guest" ]; then
    # Load credentials
    rabbitCredentials=`/bin/env python -c "import ConfigParser; c = ConfigParser.ConfigParser(); c.read('.production.cfg'); print c.get('amqp', 'username').strip() + ' ' + c.get('amqp', 'password').strip()"`
    rabbitUsername=${rabbitCredentials% *}
    rabbitPassword=${rabbitCredentials#* }
    # Initialize rabbitMQ
    /usr/sbin/rabbitmqctl stop_app
    /usr/sbin/rabbitmqctl reset
    /usr/sbin/rabbitmqctl start_app
    /usr/sbin/rabbitmqctl delete_user guest
    /usr/sbin/rabbitmqctl add_user $rabbitUsername $rabbitPassword
    /usr/sbin/rabbitmqctl set_permissions $rabbitUsername '.*' '.*' '.*'
    /bin/env python utilities/requeue.py -c production.ini
fi
