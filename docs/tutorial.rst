Tutorial
========

These exercises will introduce you to the basics of running scenarios and interpreting results.


Create an account
-----------------

#. `Open the web interface <http://october.mech.columbia.edu>`_.
#. Click `Register for an account <http://october.mech.columbia.edu/people/register>`_ at the top of the `Login <http://october.mech.columbia.edu/people/login>`_ page.
#. Check your email and click the emailed link to activate your account.


Run a demographics dataset with default parameters
--------------------------------------------------

#. Click `Create a new scenario <http://october.mech.columbia.edu/scenarios/new>`_ at the top of the `Scenarios <http://october.mech.columbia.edu>`_ page.
#. Name your scenario: Default Dataset + Default Parameters.
#. Download a `sample CSV in latitude and longitude <http://october.mech.columbia.edu/files/demographicsLL.csv>`_.  The link is to the right of *Existing locations*.
#. Examine ``demographicsLL.csv`` using a spreadsheet program.
#. Upload ``demographicsLL.csv`` to *Existing locations*.
#. Click Add this scenario to the queue.
   
.. note::

    While you are waiting for the scenario to run, you can submit another one.


Clone and set base unit household demand to 100 kWh/yr
------------------------------------------------------

#. Click `Scenarios <http://october.mech.columbia.edu>`_ at the upper right of the page.
#. Click Clone next to the scenario you just created.
#. Name your scenario: Default Dataset, Base Unit HH Demand 100.
#. Expand `Demand (household)`.
#. Click *Household unit demand per household per year* to see how it is computed.
#. Set *Household unit demand per household per year* to 100.
#. Click Add this scenario to the queue.


Clone and add Senegal Leona existing grid locations
---------------------------------------------------

#. Click `Scenarios <http://october.mech.columbia.edu>`_ at the upper right of the page.
#. Click Clone next to the scenario you just created.
#. Name your scenario: Default Dataset, Base Unit HH Demand 100, Existing Grid.
#. Download a `sample ZIP containing shapefile <http://october.mech.columbia.edu/files/networksXY.zip>`_.  The link is to the right of *Existing networks*.
#. Examine the shapefile using `qGIS <http://www.qgis.org>`_.
#. Upload the shapefile ZIP to *Existing networks*.


Clone and override nodal demand for selected towns
--------------------------------------------------

#. Click `Scenarios <http://october.mech.columbia.edu>`_ at the upper right of the page.
#. Click Clone next to the scenario you just created.
#. Name your scenario: Default Dataset, Base Unit HH Demand 100, Existing Grid, Node-Level Override.
#. Open ``demographicsLL.csv`` using a spreadsheet program.
#. Add the column header *demand > projected nodal demand per year* next to the column header *Population*.
#. Set the *demand > projected nodal demand per year* for TOBY to 11000 and SANTHIOU DIAOBE to 12000.
#. Save spreadsheet as ``demographicsLL-override.csv``.
#. Upload ``demographicsLL-override.csv`` to *Existing locations*.
#. Click Add this scenario to the queue.


Examine and compare results
---------------------------

#. Click `Scenarios <http://october.mech.columbia.edu>`_ at the upper right of the page.
#. Click View next to a scenario whose status is Done.  The scenario table at the right lists how many communities are recommended for which electricity technology, how much it will cost and how much a utility should charge per kilowatt-hour to recover its capital and recurring expenses over the time horizon.
#. Drag the mouse on the map.
#. Scroll the mouse wheel on the map.
#. Click on a community in the map or community table at the bottom to see its demand and cost projections.
#. Click on section names to expand and collapse them.
#. Click on a blank area in the map to return to the scenario table.
#. Click on a scenario name in the list on the bottom right.
#. Type *Ba* in the input box next to Filter.
