Architecture
============

Abstractly, the system takes a set of locations and populations, computes a decision metric for each location and connects selected communities to form networks.


Decision Metrics
----------------

The decision metric is used to decide between different electricity technology options: off-grid photovoltaic panels coupled with a small diesel generator, mini-grid through a large diesel generator and grid through extension of medium voltage line.

.. toctree::
    :maxdepth: 1

    metric-mvMax3
    metric-mvMax2


Understanding *mvMax*
^^^^^^^^^^^^^^^^^^^^^

The *mvMax* decision metric is the maximum length of medium voltage line for which grid extension is cheaper than standalone options.  It is best understood by example.  

    Suppose the total cost of installing off-grid technology in a community is $50,000 and mini-grid technology is $40,000 including capital and recurring costs over a time horizon of ten years.  Then the cheapest standalone option costs $40,000.  
    
    Suppose also that the cost of preparing and maintaining a community for grid connection is $34,000 excluding the cost of the actual grid extension.  That means that we have a budget of $6,000 to extend the grid to the community because if the extension cost more than $6,000 it would be more cost-effective to go with a standalone option such as off-grid or mini-grid.  
    
    If grid extension costs $10 per meter, then we can convert the budget of $6,000 into 600 meters of extension.  That means that if the community is within 600 meters of an existing grid backbone, then it is cost-effective to connect the community to the grid compared to standalone options.  The *mvMax* decision metric for the community is 600 meters.


Computing *mvMax*
^^^^^^^^^^^^^^^^^

The computation of *mvMax* takes four stages:

1. Project population and household counts.
2. Project demands.

  - Project household demand.
  - Project productive demand for powering grain grinders and water pumps.  Productive demand is proportional to household count.
  - Project social infrastructure demand.
       
    - Project commercial facility count and demand.  A commercial facility can be a vendor stall in a marketplace.
    - Project educational facility count and demand.  An educational facility can be a primary school, secondary school or university.
    - Project health facility count and demand.  A health facility can be a hospital or clinic.
    - Project public lighting facility count and demand.  Public lighting includes street lamps and traffic lights.

3. Choose system sizes for each technology.

  - Determine the needed photovoltaic panel capacity and diesel generator capacity for off-grid technology.
  - Determine the diesel generator capacity for mini-grid technology.
  - Determine the transformer capacity for grid technology.

4. Estimate initial and recurring costs for each technology.


Projecting population and household counts
""""""""""""""""""""""""""""""""""""""""""

To project population in the first year, the system takes the community's initial population, determines whether it is rural or urban using a threshold and multiplies the population by the appropriate rural or urban growth rate.  For each subsequent year, the process repeats.  Thus it is possible for a community to start with a rural growth rate but end with an urban growth rate.

To project household count, the system takes the community's projected population count at the end of the time horizon and divides it by the appropriate rural or urban mean household size.


Projecting electricity demand
"""""""""""""""""""""""""""""

To estimate each type of demand, the system multiplies the following factors:

- Demand multiplier relative to economic growth
- Demand scaling factor relative to projected population count
- Base demand in kWh/yr
- Projected facility count
  
.. index::
    single: elasticity

To compute the demand multiplier, the system multiplies elasticity of demand by economic growth rate.  *Elasticity of demand* is a measure of how much demand will change in response to economic growth.  It is a way to capture the observation that as poor households get richer, the increase in their electricity demand tends to be proportionally larger than the increase in demand when rich households get richer.  A large value for elasticity means that economic growth will result in large increases in demand, while a small value for elasticity means that economic growth will have a negligible effect on demand.  Put mathematically, elasticity is the change in electricity demand per unit of economic growth.  Thus multiplying elasticity by economic growth rate gives electricity demand growth rate.

.. index::
    single: curve, demand

To compute the demand scaling factor, the system fits a demand curve and interpolates the scaling factor using the projected population count.


Choosing system sizes
"""""""""""""""""""""


Estimating initial and recurring costs
""""""""""""""""""""""""""""""""""""""


Overriding projections using community-specific data
""""""""""""""""""""""""""""""""""""""""""""""""""""


Network Building Algorithms
---------------------------

.. toctree::
    :maxdepth: 1

    network-modKruskal
