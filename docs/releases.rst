Releases
=========

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

