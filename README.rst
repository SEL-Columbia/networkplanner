NP Electricity Infrastructure Prototyping Framework
===================================================

NetworkPlanner is a framework for planning large-scale electricity 
infrastructure projects.  Included are an example technology pricing metric 
model and a network optimization algorithm.  The framework is  
extensible so that governments can adapt the example models to fit their 
country's needs.  NetworkPlanner is developed and maintained by the 
Sustainable Engineering Lab at the Earth Institute of Columbia University.

Overview
--------

The NetworkPlanner Web application exposes the concept of a Scenario as
the main object by which users interact with the system.  Users submit
Scenarios with an associated set of inputs to be processed. The user can 
retrieve processed scenario data or view it via the web-site.  

Dependencies
------------

NetworkPlanner depends on the following system and python tools

- System Tools
::

    GDAL 
    Libspatialindex (only for network model)
    PostgreSQL (only for production website)
    RabbitMQ (only for distributed system)


- Python Tools (not everything, see requirements.txt for all)
::

   numpy/scipy
   shapely

Setup
-----

The recommended setup procedure for NetworkPlanner depends on the mode of
operation.  

Development and CLI
~~~~~~~~~~~~~~~~~~~

For Development and "CLI" (command-line) mode, the following script can be 
used as a guide to create a working environment on Debian based systems 
(including Ubuntu).  

- Sample bash script for basic Debian/Ubuntu setup
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
    
    # NOTE:  Depending on your default user environment variables, you may need to set
    # the LD_LIBRARY_PATH in order for networkplanner to reference libspatialindex properly
    # Here are the contents of my $VIRTUAL_ENV/bin/postactivate file:
    
    export OLD_LD_LIBRARY_PATH=$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
    
    # and the $VIRTUAL_ENV/bin/predeactivate file:
    
    export LD_LIBRARY_PATH=$OLD_LD_LIBRARY_PATH
    unset OLD_LD_LIBRARY_PATH


Modes of Operation
------------------

NetworkPlanner consists of 2 main modules (the Metric "builder" and the Network
"builder").  These are exposed through both command-line interfaces and a web
interface that can be deployed as a "Standalone" server or as a set of distributed
processing servers.  

CLI (aka command-line)
~~~~~~~~~~~~~~~~~~~~~

CLI mode allows a user to run the various utility scripts provided as 
part of NetworkPlanner without running a web/application server.  This is 
useful for developing models and analyzing their output.  These scripts reside 
in the utilities directory and can be run via python.

- Sample Commands
::

    # Run metric model on a set of demand nodes (using mvMax5 model)
    # The output can be loaded as an R or Pandas dataframe for analysis
    python utilities/build_demand.py mvMax5 sample_metric_params.json test_data/sample_demand_nodes.csv > sample_demand_out.csv

    # Run full scenario (including network builder) on a set of demand nodes
    # (the results will end up in the mv5_run directory as spec'd by the 5th param)
    python utilities/run_scenario.py mvMax5 sample_metric_params.json modKruskal network_params.json mv5_run test_data/sample_demand_nodes.csv

    # Create a dot graph for the dependencies of the MiniGrid RecurringCost 
    # variable of the mvMax4 model 
    # The dot file can be passed to graphviz utilities to render the graphs as png, svg, pdf...
    python utilities/model_var_dependencies.py mvMax4 costMiniGrid.MiniGridSystemRecurringCostPerYear mv4_mg_rec.dot class

    # Create a flat list of class, option/section, alias name mappings of all 
    # variables "under" Metric for mvMax5
    python utilities/write_variable_fields.py mvMax5 Metric > mapping_mvmax5.csv


Development
~~~~~~~~~~~

Development mode runs the NetworkPlanner web-site via the Paste_  server with 
debugging enabled.  This mode is useful for developing and testing the 
system and web interface.  SQLite is the default database for this mode.

- Some useful commands:  
::
    
    # Run the development server via paster 
    # 'ds' for development server
    ./restart ds 

    # Generate the docs
    ./restart docs

    # start interactive python session for working with 
    # web app in development mode
    paster shell development.ini

    # Process scenarios submitted


Production (Standalone and Distributed)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The NetworkPlanner web application can be deployed as a standalone server or
as a set of distributed processors:

- Standalone:  Single server handling all requests

- Distributed:  

  Master server handling main interface requests and then
  distributing the processing of scenarios among processor nodes.  
  Utilizes RabbitMQ to synchronize between Master and Processors.  
   
For Production deployment, we utilize a combination of Chef_ and Fabric_ to
standardize and automate deployment.  Production deployments utilize 
Postgresql as the main database.  

Please refer to the networkplanner-devops_ repository for details and 
instructions.  

Troubleshooting
---------------

- Run the following script if RabbitMQ seems down 
::

    deployment/cluster-queue-reset.sh

.. _Paste:  http://pythonpaste.org/
.. _Chef:  docs.opscode.com
.. _Fabric:  fabfile.org
.. _networkplanner-devops:  https://github.com/SEL-Columbia/networkplanner-devops
