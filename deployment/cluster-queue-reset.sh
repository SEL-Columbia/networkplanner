#!/bin/bash
if [ ! -f .production.cfg ]; then
    echo "Please run this script in a directory containing .production.cfg"
fi
# If rabbitMQ has been reset,
if sudo rabbitmqctl list_users | grep '^guest'; then
    # Load credentials
    rabbitCredentials=`python -c "import ConfigParser; c = ConfigParser.ConfigParser(); c.read('.production.cfg'); print c.get('amqp', 'username').strip() + ' ' + c.get('amqp', 'password').strip()"`
    rabbitUsername=${rabbitCredentials% *}
    rabbitPassword=${rabbitCredentials#* }
    # Initialize rabbitMQ
    sudo rabbitmqctl stop_app
    sudo rabbitmqctl reset
    sudo rabbitmqctl start_app
    sudo rabbitmqctl delete_user guest
    sudo rabbitmqctl add_user $rabbitUsername $rabbitPassword
    sudo rabbitmqctl set_permissions $rabbitUsername '.*' '.*' '.*'
    python utilities/requeue.py -c production.ini
fi
