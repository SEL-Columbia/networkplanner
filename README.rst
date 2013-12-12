NP Electricity Infrastructure Prototyping Framework
===================================================
NetworkPlanner is a framework for planning large-scale electricity infrastructure projects.  
Included are an example technology pricing metric model and a network optimization algorithm.  
The framework is easily extensible so that governments can adapt the example models to fit their country's needs.  
NetworkPlanner is developed and maintained by the Sustainable Engineering Lab at the Earth Institute of Columbia University.

Dependencies
------------

NetworkPlanner depends on the following system and python tools

- System Tools
::
    GDAL 
    Libspatialindex (only for network model)
    PostgreSQL (only for website)
    RabbitMQ (only for distributed system)


- Python Tools (not everything, see requirements.txt for all)
::
   numpy/scipy
   shapely

Setup
-----

These are setup instructions for Debian based systems (including Ubuntu).  
These have only been tested on Ubuntu 12.04, but should be similar for other Debian systems.

- Sample bash script for Debian/Ubuntu install and reference
::

    # setup system level packages
    sudo apt-get -y install git python-pip python-dev libgdal-dev build-essential
    # for scipy
    sudo apt-get -y install gfortran libopenblas-dev liblapack-dev

    # libspatialindex (only required for network model)
    mkdir -p tmp
    cd tmp
    git clone git://github.com/libspatialindex/libspatialindex.git
    sudo apt-get install -y automake libtool
    (cd libspatialindex && ./autogen.sh && ./configure && make && sudo make install)
    sudo ldconfig
    cd

    git clone https://github.com/SEL-Columbia/networkplanner.git np
    # git clone git@github.com:SEL-Columbia/networkplanner.git np

    # install virtualenv and virtualenvwrapper (see http://virtualenvwrapper.readthedocs.org)
    # YMMV 
    # This is optional if you don't mind intermingled python packages on your system
    sudo apt-get -y install python-virtualenv
    sudo pip install virtualenvwrapper
    # setup your bashrc to source virtualenvwrapper
    if ! grep 'virtualenvwrapper\.sh' .bashrc; 
    then
    cat >> .bashrc << EOF
    . `which virtualenvwrapper.sh`
    EOF
    fi
    . `which virtualenvwrapper.sh` # source it for the session (not needed for future sessions)
    if ! workon np > /dev/null
    then
        mkvirtualenv --system-site-packages np # from here on, working in np virtualenv
        cd np 
        setvirtualenvproject # from here on you can enter 'workon np' to work in the np virtualenv
    fi

    # setup project specific python packages
    pip install -r requirements.txt

    # only required for network model
    pip install -r requirements_network.txt 


Running "standalone" Commands
-----------------------------
There are several utilities that run independent of the web-site system.
These reside in the utilities directory and can be run via python.

- Sample Commands
::
    # Run metric model on a set of demand nodes (using mvMax5 model)
    python utilities/build_demand.py test_data/sample_demand_nodes.csv mvMax5 sample_metric_params.json > sample_demand_out.csv

    # Create a dot graph for the dependencies of the MiniGrid RecurringCost 
    # variable of the mvMax4 model 
    python utilities/model_var_dependencies.py mvMax4 costMiniGrid.MiniGridSystemRecurringCostPerYear mv4_mg_rec.dot class

    # Create a flat list of class, option/section, alias name mappings of all 
    # variables "under" Metric for mvMax5
    python utilities/write_variable_fields.py mvMax5 Metric > mapping_mvmax5.csv


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
