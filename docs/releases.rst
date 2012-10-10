Releases
=========

v0.9.4M
----------------

Significant reduction in memory consumption

- Represent the candidate segments as a numpy RecordArray of
  node_id1, node_id2 and weight.

- This reduces the memory required from 300 bytes to 8 bytes 
  per candidate segment.  The candidate segments dominate 
  the memory required when the number of nodes n grows large.
  (there are (n*(n-1))/2 candidate segments).  

- A comparison of memory consumption for a scenario with the 
  5577 input nodes:

======== ===================== ============================
Version  Max NP Memory Used    Max Candidate Segment Memory
======== ===================== ============================
0.9.4    14.8G                 7.85 G
0.9.4M   1.2G (1/12 reduction) 124.4 M (1/60 reduction)
======== ===================== ============================

.. note::
   
    If the demand is high and many of the candidate segments
    pass the mvMax test, then more memory will be used.  This
    is because we still instantiate segments to test whether 
    they can be added to the network.  If this becomes an 
    issue, we can extend the numpy based segment representation 
    deeper into the network algorithm (which also makes sense 
    from an architectural consistency perspective).  
    

v0.9.4
----------------

Significant performance improvement in terms of computation time.

- Utilize R-Tree spatial index to speedup intersection test within network 
  generation algorithm.  

   
- Theoretically, the worst-case run-time went from :math:`N^3` to 
  :math:`N^2 log(N)` (where N is the number of input nodes).  
  So it's a max of :math:`\frac{N}{log(N)}` faster).

- Practically, it's > 10x faster for "large" scenarios.

- Some numbers for specific scenarios:

===== ================== ============ ==========================
Nodes In + Out Grid Size Old Run-Time New Run-Time
===== ================== ============ ==========================
937   3189 (low demand)  327 seconds  151 seconds (2.16x faster) 
937   3696               339 minutes  27 minutes (12.5x faster) 
5577  4641               3966 minutes 276 minutes (14.4x faster) 
===== ================== ============ ==========================

.. note::
  
    All of the above scenarios ran on an Amazon m2.2xlarge instance with
    34.2G of RAM and 4 2.67 GHz processors.  

- Improved test coverage, including controller based scenario run with 
  output comparison to known "good" scenario.  

v0.9.3
----------------

Address backward compatibility issues

- Moved mvMax3 model changes to a new mvMax4
  (new models allow us to preserve backward compatibility)
 
- Merged in UI design changes from Roger

