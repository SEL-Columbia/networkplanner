NP Electricity Infrastructure Prototyping Framework
===================================================
NetworkPlanner is a framework for planning large-scale electricity infrastructure projects.  Included are an example technology pricing metric model and a network optimization algorithm.  The framework is easily extensible so that governments can adapt the example models to fit their country's needs.  NetworkPlanner is developed and maintained by the Modi Research Group at the Earth Institute of Columbia University.


Run development server
----------------------
This option enables debugging and is useful for creating new models or changing the framework code.

1. Install dependencies.
::

    su -c "deployment/dependencies-setup.sh"

2. Generate documentation.
::

    ./restart docs

3. Run development server.
::

    ./restart ds


Run production server on a single computer
------------------------------------------
This option disables debugging and is useful for production release testing.

1. Install dependencies.
::

    su -c "deployment/dependencies-setup.sh"

2. Prepare PostgreSQL database and access credentials.
::

    sudo service postgresql start
    sudo su postgres
      createdb np
      createuser np
      psql
        grant all on database np to np;
        alter role np password 'AyfNFioDbFJDNyjaQK3xHDtUZIcHdU0b'
      vim data/pg_hba.conf            # Set METHOD to md5
      exit
    sudo service postgresql restart
    exit


3. Create configuration file.
::

    cp default.cfg .production.cfg
    vim .production.cfg

4. Configure nginx server.
::

    su
        yum remove -y httpd
        yum install -y nginx
        vim /etc/nginx/nginx.conf           # See deployment/nginx.conf
        service nginx restart
        exit

5. Run single production server.
::

    ./restart ss


Run production server on a cluster of computers
-----------------------------------------------
This option disables debugging and is useful for production deployment.
Run these commands after you have performed steps 1 - 4 for running a 
production server on a single computer.

1. Run cluster production server.
::

    ./restart cs

2. Run the following script on each cluster machine.
::

    cluster-processor-setup.sh              # Change 134f to your desired username

Troubleshooting
---------------

- Run the following script if RabbitMQ seems down 
::

    deployment/cluster-queue-reset.sh
