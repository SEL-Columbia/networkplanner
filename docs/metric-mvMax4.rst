Metric Model mvMax4
===================
- :ref:`mvmax4-metric`
- :ref:`mvmax4-offgridsystemtotal`
- :ref:`mvmax4-offgridsystemtotalinitialcost`
- :ref:`mvmax4-offgridsystemtotaldiscounteddieselcost`
- :ref:`mvmax4-offgridsystemtotaldiscounteddieselfuelcost`
- :ref:`mvmax4-offgridsystemtotaldiscountedrecurringcost`
- :ref:`mvmax4-offgridsystemtotallevelizedcost`
- :ref:`mvmax4-minigridsystemtotal`
- :ref:`mvmax4-minigridsystemtotalinitialcost`
- :ref:`mvmax4-minigridsystemtotaldiscounteddieselfuelcost`
- :ref:`mvmax4-minigridsystemtotaldiscountedrecurringcost`
- :ref:`mvmax4-minigridsystemtotallevelizedcost`
- :ref:`mvmax4-gridsystemtotal`
- :ref:`mvmax4-gridsystemtotalinitialcost`
- :ref:`mvmax4-gridsystemtotaldiscountedrecurringcost`
- :ref:`mvmax4-gridsystemtotallevelizedcost`
- :ref:`mvmax4-gridsystemtotalexistingnetworklength`
- :ref:`mvmax4-gridsystemtotalproposednetworklength`


You can override the value of any variable in the model on a node-by-node basis.  To perform a node-level override, use the aliases in the following table as additional columns in your spreadsheet or fields in your shapefile.  Both long and short aliases are recognized.

=============================================================================================================================================================================================================================== ============== ==================================
Long alias                                                                                                                                                                                                                      Short alias    Units                             
=============================================================================================================================================================================================================================== ============== ==================================
:ref:`finance > discounted cash flow factor <mvmax4-finance-discountedcashflowfactor>`                                                                                                                                          dcff                                             
:ref:`finance > economic growth rate per year <mvmax4-finance-economicgrowthrateperyear>`                                                                                                                                       economic_g     fraction per year                 
:ref:`finance > elasticity of electricity demand <mvmax4-finance-elasticityofelectricitydemand>`                                                                                                                                elasticity                                       
:ref:`finance > electricity demand growth rate per year <mvmax4-finance-electricitydemandgrowthrateperyear>`                                                                                                                    dem_g          fraction per year                 
:ref:`finance > electricity demand multiplier <mvmax4-finance-electricitydemandmultiplier>`                                                                                                                                     demf                                             
:ref:`finance > interest rate per year <mvmax4-finance-interestrateperyear>`                                                                                                                                                    interest_g     fraction per year                 
:ref:`finance > time horizon <mvmax4-finance-timehorizon>`                                                                                                                                                                      time           years                             
:ref:`demographics > is rural <mvmax4-demographics-isrural>`                                                                                                                                                                    rural          binary                            
:ref:`demographics > mean household size <mvmax4-demographics-meanhouseholdsize>`                                                                                                                                               ho_size        person count                      
:ref:`demographics > mean household size (rural) <mvmax4-demographics-ruralmeanhouseholdsize>`                                                                                                                                  ho_size_r      person count                      
:ref:`demographics > mean household size (urban) <mvmax4-demographics-urbanmeanhouseholdsize>`                                                                                                                                  ho_size_u      person count                      
:ref:`demographics > mean interhousehold distance <mvmax4-demographics-meaninterhouseholddistance>`                                                                                                                             mid            meters                            
:ref:`demographics > population count <mvmax4-demographics-populationcount>`                                                                                                                                                    pop population person count                      
:ref:`demographics > population growth rate per year (rural) <mvmax4-demographics-ruralpopulationgrowthrateperyear>`                                                                                                            pop_g_r        fraction per year                 
:ref:`demographics > population growth rate per year (urban) <mvmax4-demographics-urbanpopulationgrowthrateperyear>`                                                                                                            pop_g_u        fraction per year                 
:ref:`demographics > projected household count <mvmax4-demographics-projectedhouseholdcount>`                                                                                                                                   p_ho           household count                   
:ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`                                                                                                                                 p_pop          person count                      
:ref:`demographics > projected population counts <mvmax4-demographics-projectedpopulationcounts>`                                                                                                                               p_pops         person count list                 
:ref:`demographics > urban population threshold <mvmax4-demographics-urbanpopulationthreshold>`                                                                                                                                 u_pop_thre     person count                      
:ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`                                                                                                                                     p_dem          kilowatt-hours per year           
:ref:`demand > projected nodal discounted demand <mvmax4-demand-projectednodaldiscounteddemand>`                                                                                                                                p_dem_d        kilowatt-hours                    
:ref:`demand (peak) > demand to peak demand conversion factor <mvmax4-demand-demandtopeakdemandconversionfactor>`                                                                                                               dem_pkdemf                                       
:ref:`demand (peak) > peak demand as fraction of nodal demand occurring during peak hours <mvmax4-demand-peakdemandasfractionofnodaldemandoccurringduringpeakhours>`                                                            pkdemf                                           
:ref:`demand (peak) > peak demand as fraction of nodal demand occurring during peak hours (rural) <mvmax4-demand-ruralpeakdemandasfractionofnodaldemandoccurringduringpeakhours>`                                               pkdemf_r                                         
:ref:`demand (peak) > peak demand as fraction of nodal demand occurring during peak hours (urban) <mvmax4-demand-urbanpeakdemandasfractionofnodaldemandoccurringduringpeakhours>`                                               pkdemf_u                                         
:ref:`demand (peak) > peak electrical hours of operation per year <mvmax4-demand-peakelectricalhoursofoperationperyear>`                                                                                                        pkel_hr        hours per year                    
:ref:`demand (peak) > projected peak commercial facility demand <mvmax4-demand-projectedpeakcommercialfacilitydemand>`                                                                                                          p_pkdem_co     kilowatts                         
:ref:`demand (peak) > projected peak nodal demand <mvmax4-demand-projectedpeaknodaldemand>`                                                                                                                                     p_pkdem        kilowatts                         
:ref:`demand (peak) > projected peak productive demand <mvmax4-demand-projectedpeakproductivedemand>`                                                                                                                           p_pkdem_pr     kilowatts                         
:ref:`demand (household) > demand curve <mvmax4-demand-householddemandcurve>`                                                                                                                                                   ho_dc                                            
:ref:`demand (household) > demand curve points (population and multiplier) <mvmax4-demand-householddemandcurvepoints>`                                                                                                          ho_dc_pts      population and multiplier list    
:ref:`demand (household) > demand curve type <mvmax4-demand-householddemandcurvetype>`                                                                                                                                          ho_dc_t                                          
:ref:`demand (household) > household unit demand per household per year <mvmax4-demand-householdunitdemandperhouseholdperyear>`                                                                                                 ho_dc_unit     kilowatt-hours per year           
:ref:`demand (household) > projected household demand per year <mvmax4-demand-projectedhouseholddemandperyear>`                                                                                                                 p_dem_ho       kilowatt-hours per year           
:ref:`demand (household) > target household count <mvmax4-demand-targethouseholdcount>`                                                                                                                                         ct_hh_t        households                        
:ref:`demand (household) > target household penetration rate <mvmax4-demand-targethouseholdpenetrationrate>`                                                                                                                                                                     
:ref:`demand (productive) > demand curve <mvmax4-demand-productivedemandcurve>`                                                                                                                                                 pr_dc                                            
:ref:`demand (productive) > demand curve points (population and multiplier) <mvmax4-demand-productivedemandcurvepoints>`                                                                                                        pr_dc_pts      population and multiplier list    
:ref:`demand (productive) > demand curve type <mvmax4-demand-productivedemandcurvetype>`                                                                                                                                        pr_dc_t                                          
:ref:`demand (productive) > productive unit demand per household per year <mvmax4-demand-productiveunitdemandperhouseholdperyear>`                                                                                              pr_dc_unit     kilowatt-hours per year           
:ref:`demand (productive) > projected productive demand <mvmax4-demand-projectedproductivedemandperyear>`                                                                                                                       p_dem_pr       kilowatt-hours per year           
:ref:`demand (social infrastructure) > commercial facility count curve <mvmax4-demand-commercialfacilitycountcurve>`                                                                                                            co_cc                                            
:ref:`demand (social infrastructure) > commercial facility count curve points (population and facility count) <mvmax4-demand-commercialfacilitycountcurvepoints>`                                                               co_cc_pts      population and facility count list
:ref:`demand (social infrastructure) > commercial facility count curve type <mvmax4-demand-commercialfacilitycountcurvetype>`                                                                                                   co_cc_t                                          
:ref:`demand (social infrastructure) > commercial facility unit demand per commercial facility per year <mvmax4-demand-commercialfacilityunitdemandpercommercialfacilityperyear>`                                               co_dc_unit     kilowatt-hours per year           
:ref:`demand (social infrastructure) > demand curve <mvmax4-demand-socialinfrastructuredemandcurve>`                                                                                                                            so_dc                                            
:ref:`demand (social infrastructure) > demand curve points (population and multiplier) <mvmax4-demand-socialinfrastructuredemandcurvepoints>`                                                                                   so_dc_pts      population and multiplier list    
:ref:`demand (social infrastructure) > demand curve type <mvmax4-demand-socialinfrastructuredemandcurvetype>`                                                                                                                   so_dc_t                                          
:ref:`demand (social infrastructure) > education facility count curve <mvmax4-demand-educationfacilitycountcurve>`                                                                                                              ed_cc                                            
:ref:`demand (social infrastructure) > education facility count curve points (population and facility count) <mvmax4-demand-educationfacilitycountcurvepoints>`                                                                 ed_cc_pts      population and facility count list
:ref:`demand (social infrastructure) > education facility count curve type <mvmax4-demand-educationfacilitycountcurvetype>`                                                                                                     ed_cc_t                                          
:ref:`demand (social infrastructure) > education facility unit demand per education facility per year <mvmax4-demand-educationfacilityunitdemandpereducationfacilityperyear>`                                                   ed_dc_unit     kilowatt-hours per year           
:ref:`demand (social infrastructure) > health facility count curve <mvmax4-demand-healthfacilitycountcurve>`                                                                                                                    he_cc                                            
:ref:`demand (social infrastructure) > health facility count curve points (population and facility count) <mvmax4-demand-healthfacilitycountcurvepoints>`                                                                       he_cc_pts      population and facility count list
:ref:`demand (social infrastructure) > health facility count curve type <mvmax4-demand-healthfacilitycountcurvetype>`                                                                                                           he_cc_t                                          
:ref:`demand (social infrastructure) > health facility unit demand per health facility per year <mvmax4-demand-healthfacilityunitdemandperhealthfacilityperyear>`                                                               he_dc_unit     kilowatt-hours per year           
:ref:`demand (social infrastructure) > projected commercial facility count <mvmax4-demand-projectedcommercialfacilitycount>`                                                                                                    p_co           commercial facility count         
:ref:`demand (social infrastructure) > projected commercial facility demand per year <mvmax4-demand-projectedcommercialfacilitydemandperyear>`                                                                                  p_dem_co       kilowatt-hours per year           
:ref:`demand (social infrastructure) > projected education facility count <mvmax4-demand-projectededucationfacilitycount>`                                                                                                      p_ed           education facility count          
:ref:`demand (social infrastructure) > projected education facility demand per year <mvmax4-demand-projectededucationfacilitydemandperyear>`                                                                                    p_dem_ed       kilowatt-hours per year           
:ref:`demand (social infrastructure) > projected health facility count <mvmax4-demand-projectedhealthfacilitycount>`                                                                                                            p_he           health facility count             
:ref:`demand (social infrastructure) > projected health facility demand per year <mvmax4-demand-projectedhealthfacilitydemandperyear>`                                                                                          p_dem_he       kilowatt-hours per year           
:ref:`demand (social infrastructure) > projected public lighting facility count <mvmax4-demand-projectedpubliclightingfacilitycount>`                                                                                           p_li           public lighting facility count    
:ref:`demand (social infrastructure) > projected public lighting facility demand per year <mvmax4-demand-projectedpubliclightingfacilitydemandperyear>`                                                                         p_dem_li       kilowatt-hours per year           
:ref:`demand (social infrastructure) > public lighting facility count curve <mvmax4-demand-publiclightingfacilitycountcurve>`                                                                                                   li_cc                                            
:ref:`demand (social infrastructure) > public lighting facility count curve points (population and facility count) <mvmax4-demand-publiclightingfacilitycountcurvepoints>`                                                      li_cc_pts      population and facility count list
:ref:`demand (social infrastructure) > public lighting facility count curve type <mvmax4-demand-publiclightingfacilitycountcurvetype>`                                                                                          li_cc_t                                          
:ref:`demand (social infrastructure) > public lighting facility unit demand per public lighting facility per year <mvmax4-demand-publiclightingfacilityunitdemandperpubliclightingfacilityperyear>`                             li_dc_unit     kilowatt-hours per year           
:ref:`distribution > low voltage line cost per meter <mvmax4-costdistribution-lowvoltagelinecostpermeter>`                                                                                                                      di_ll_cm       dollars per meter                 
:ref:`distribution > low voltage line equipment cost per connection <mvmax4-costdistribution-lowvoltagelineequipmentcostperconnection>`                                                                                         di_le_cc       dollars per connection            
:ref:`distribution > low voltage line equipment operations and maintenance cost as fraction of equipment cost <mvmax4-costdistribution-lowvoltagelineequipmentoperationsandmaintenancecostperyearasfractionofequipmentcost>`    di_le_omf                                        
:ref:`distribution > low voltage line initial cost <mvmax4-costdistribution-lowvoltagelineinitialcost>`                                                                                                                         di_ll_ini      dollars                           
:ref:`distribution > low voltage line length <mvmax4-costdistribution-lowvoltagelinelength>`                                                                                                                                    di_ll_len      meters                            
:ref:`distribution > low voltage line lifetime <mvmax4-costdistribution-lowvoltagelinelifetime>`                                                                                                                                di_ll_life     years                             
:ref:`distribution > low voltage line operations and maintenance cost per year <mvmax4-costdistribution-lowvoltagelineoperationsandmaintenancecostperyear>`                                                                     di_ll_om       dollars per year                  
:ref:`distribution > low voltage line operations and maintenance cost per year as fraction of line cost <mvmax4-costdistribution-lowvoltagelineoperationsandmaintenancecostperyearasfractionoflinecost>`                        di_ll_omf                                        
:ref:`distribution > low voltage line recurring cost per year <mvmax4-costdistribution-lowvoltagelinerecurringcostperyear>`                                                                                                     di_ll_rec      dollars per year                  
:ref:`distribution > low voltage line replacement cost per year <mvmax4-costdistribution-lowvoltagelinereplacementcostperyear>`                                                                                                 di_ll_rep      dollars per year                  
:ref:`system (off-grid) > available system capacities (diesel generator) <mvmax4-costoffgrid-dieselgeneratoravailablesystemcapacities>`                                                                                         og_dg_cps      kilowatts list                    
:ref:`system (off-grid) > available system capacities (photovoltaic panel) <mvmax4-costoffgrid-photovoltaicpanelavailablesystemcapacities>`                                                                                     og_pp_cps      kilowatts list                    
:ref:`system (off-grid) > diesel component initial cost <mvmax4-costoffgrid-dieselcomponentinitialcost>`                                                                                                                        og_d_ini       dollars                           
:ref:`system (off-grid) > diesel component recurring cost per year <mvmax4-costoffgrid-dieselcomponentrecurringcostperyear>`                                                                                                    og_d_rec       dollars per year                  
:ref:`system (off-grid) > diesel fuel cost per year <mvmax4-costoffgrid-dieselfuelcostperyear>`                                                                                                                                 og_fl          dollars per year                  
:ref:`system (off-grid) > diesel generator actual system capacity <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacity>`                                                                                                     og_dg_acp      kilowatts                         
:ref:`system (off-grid) > diesel generator actual system capacity counts <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacitycounts>`                                                                                        og_dg_acps     capacity count list               
:ref:`system (off-grid) > diesel generator cost <mvmax4-costoffgrid-dieselgeneratorcost>`                                                                                                                                       og_dg_ini      dollars                           
:ref:`system (off-grid) > diesel generator desired system capacity <mvmax4-costoffgrid-dieselgeneratordesiredsystemcapacity>`                                                                                                   og_dg_dcp      kilowatts                         
:ref:`system (off-grid) > diesel generator hours of operation per year (effective) <mvmax4-costoffgrid-dieselgeneratoreffectivehoursofoperationperyear>`                                                                        og_dg_efhr     hours per year                    
:ref:`system (off-grid) > diesel generator hours of operation per year (minimum) <mvmax4-costoffgrid-dieselgeneratorminimumhoursofoperationperyear>`                                                                            og_dg_mnhr     hours per year                    
:ref:`system (off-grid) > diesel generator installation cost <mvmax4-costoffgrid-dieselgeneratorinstallationcost>`                                                                                                              og_dg_i        dollars                           
:ref:`system (off-grid) > diesel generator operations and maintenance cost per year <mvmax4-costoffgrid-dieselgeneratoroperationsandmaintenancecostperyear>`                                                                    og_dg_om       dollars per year                  
:ref:`system (off-grid) > diesel generator replacement cost per year <mvmax4-costoffgrid-dieselgeneratorreplacementcostperyear>`                                                                                                og_dg_rep      dollars per year                  
:ref:`system (off-grid) > peak sun hours per year <mvmax4-costoffgrid-peaksunhoursperyear>`                                                                                                                                     pksu_hr        hours per year                    
:ref:`system (off-grid) > photovoltaic balance cost <mvmax4-costoffgrid-photovoltaicbalancecost>`                                                                                                                               og_px_ini      dollars                           
:ref:`system (off-grid) > photovoltaic balance cost as fraction of panel cost <mvmax4-costoffgrid-photovoltaicbalancecostasfractionofpanelcost>`                                                                                og_px_cf                                         
:ref:`system (off-grid) > photovoltaic balance lifetime <mvmax4-costoffgrid-photovoltaicbalancelifetime>`                                                                                                                       og_px_life     years                             
:ref:`system (off-grid) > photovoltaic balance replacement cost per year <mvmax4-costoffgrid-photovoltaicbalancereplacementcostperyear>`                                                                                        og_px_rep      dollars per year                  
:ref:`system (off-grid) > photovoltaic battery cost <mvmax4-costoffgrid-photovoltaicbatterycost>`                                                                                                                               og_pb_ini      dollars                           
:ref:`system (off-grid) > photovoltaic battery cost per kilowatt-hour <mvmax4-costoffgrid-photovoltaicbatterycostperkilowatthour>`                                                                                              og_pb_ckwh     dollars per kilowatt-hour         
:ref:`system (off-grid) > photovoltaic battery kilowatt-hours per photovoltaic component kilowatt <mvmax4-costoffgrid-photovoltaicbatterykilowatthoursperphotovoltaiccomponentkilowatt>`                                        og_pb_hkw      kilowatt-hours per kilowatt       
:ref:`system (off-grid) > photovoltaic battery lifetime <mvmax4-costoffgrid-photovoltaicbatterylifetime>`                                                                                                                       og_pb_life     years                             
:ref:`system (off-grid) > photovoltaic battery replacement cost per year <mvmax4-costoffgrid-photovoltaicbatteryreplacementcostperyear>`                                                                                        og_pb_rep      dollars per year                  
:ref:`system (off-grid) > photovoltaic component efficiency loss <mvmax4-costoffgrid-photovoltaiccomponentefficiencyloss>`                                                                                                      og_p_loss      fraction                          
:ref:`system (off-grid) > photovoltaic component initial cost <mvmax4-costoffgrid-photovoltaiccomponentinitialcost>`                                                                                                            og_p_ini       dollars                           
:ref:`system (off-grid) > photovoltaic component operations and maintenance cost per year <mvmax4-costoffgrid-photovoltaiccomponentoperationsandmaintenancecostperyear>`                                                        og_p_om        dollars per year                  
:ref:`system (off-grid) > photovoltaic component operations and maintenance cost per year as fraction of component cost <mvmax4-costoffgrid-photovoltaiccomponentoperationsandmaintenancecostperyearasfractionofcomponentcost>` og_p_omf                                         
:ref:`system (off-grid) > photovoltaic component recurring cost per year <mvmax4-costoffgrid-photovoltaiccomponentrecurringcostperyear>`                                                                                        og_p_rec       dollars per year                  
:ref:`system (off-grid) > photovoltaic panel actual capacity <mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacity>`                                                                                                        og_pp_acp      kilowatts                         
:ref:`system (off-grid) > photovoltaic panel actual capacity counts <mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacitycounts>`                                                                                           og_pp_acps     capacity count list               
:ref:`system (off-grid) > photovoltaic panel cost <mvmax4-costoffgrid-photovoltaicpanelcost>`                                                                                                                                   og_pp_ini      dollars                           
:ref:`system (off-grid) > photovoltaic panel cost per photovoltaic component kilowatt <mvmax4-costoffgrid-photovoltaicpanelcostperphotovoltaiccomponentkilowatt>`                                                               og_pp_ckw      dollars per kilowatt              
:ref:`system (off-grid) > photovoltaic panel desired capacity <mvmax4-costoffgrid-photovoltaicpaneldesiredsystemcapacity>`                                                                                                      og_pp_dcp      kilowatts                         
:ref:`system (off-grid) > photovoltaic panel lifetime <mvmax4-costoffgrid-photovoltaicpanellifetime>`                                                                                                                           og_pp_life     years                             
:ref:`system (off-grid) > photovoltaic panel replacement cost per year <mvmax4-costoffgrid-photovoltaicpanelreplacementcostperyear>`                                                                                            og_pp_rep      dollars per year                  
:ref:`system (off-grid) > system initial cost <mvmax4-costoffgrid-offgridsysteminitialcost>`                                                                                                                                    og_ini         dollars                           
:ref:`system (off-grid) > system nodal discounted cost <mvmax4-costoffgrid-offgridsystemnodaldiscountedcost>`                                                                                                                   og_nod_d       dollars                           
:ref:`system (off-grid) > system nodal levelized cost <mvmax4-costoffgrid-offgridsystemnodallevelizedcost>`                                                                                                                     og_nod_lev     dollars per kilowatt-hour         
:ref:`system (off-grid) > system recurring cost per year <mvmax4-costoffgrid-offgridsystemrecurringcostperyear>`                                                                                                                og_rec         dollars per year                  
:ref:`system (off-grid) > system total <mvmax4-offgridsystemtotal>`                                                                                                                                                             og_ct          count                             
:ref:`system (off-grid) > system total discounted cost <mvmax4-offgridsystemtotaldiscountedcost>`                                                                                                                               og_tot_d       dollars                           
:ref:`system (off-grid) > system total discounted demand <mvmax4-offgridsystemtotaldiscounteddemand>`                                                                                                                           og_dem_d       kilowatt-hours                    
:ref:`system (off-grid) > system total discounted diesel cost <mvmax4-offgridsystemtotaldiscounteddieselcost>`                                                                                                                  og_tot_ddc     dollars                           
:ref:`system (off-grid) > system total discounted diesel fuel cost <mvmax4-offgridsystemtotaldiscounteddieselfuelcost>`                                                                                                         og_tot_ddfc    dollars                           
:ref:`system (off-grid) > system total discounted recurring cost <mvmax4-offgridsystemtotaldiscountedrecurringcost>`                                                                                                            og_tot_drc     dollars                           
:ref:`system (off-grid) > system total initial cost <mvmax4-offgridsystemtotalinitialcost>`                                                                                                                                     og_tot_i       dollars                           
:ref:`system (off-grid) > system total levelized cost <mvmax4-offgridsystemtotallevelizedcost>`                                                                                                                                 og_tot_lev     dollars per kilowatt-hour         
:ref:`system (mini-grid) > available system capacities (diesel generator) <mvmax4-costminigrid-dieselgeneratoravailablesystemcapacities>`                                                                                       mg_dg_cps      kilowatts list                    
:ref:`system (mini-grid) > diesel fuel cost per liter <mvmax4-costminigrid-dieselfuelcostperliter>`                                                                                                                             mg_fl_cl       dollars per liter                 
:ref:`system (mini-grid) > diesel fuel cost per year <mvmax4-costminigrid-dieselfuelcostperyear>`                                                                                                                               mg_fl          dollars per year                  
:ref:`system (mini-grid) > diesel fuel liters consumed per kilowatt-hour <mvmax4-costminigrid-dieselfuellitersconsumedperkilowatthour>`                                                                                         mg_fl_lkwh     liters per kilowatt-hour          
:ref:`system (mini-grid) > diesel generator actual system capacity <mvmax4-costminigrid-dieselgeneratoractualsystemcapacity>`                                                                                                   mg_dg_acp      kilowatts                         
:ref:`system (mini-grid) > diesel generator actual system capacity counts <mvmax4-costminigrid-dieselgeneratoractualsystemcapacitycounts>`                                                                                      mg_dg_acps     capacity count list               
:ref:`system (mini-grid) > diesel generator cost <mvmax4-costminigrid-dieselgeneratorcost>`                                                                                                                                     mg_dg_ini      dollars                           
:ref:`system (mini-grid) > diesel generator cost per diesel system kilowatt <mvmax4-costminigrid-dieselgeneratorcostperdieselsystemkilowatt>`                                                                                   mg_dg_ck       dollars per kilowatt              
:ref:`system (mini-grid) > diesel generator desired system capacity <mvmax4-costminigrid-dieselgeneratordesiredsystemcapacity>`                                                                                                 mg_dg_dcp      kilowatts                         
:ref:`system (mini-grid) > diesel generator hours of operation per year (effective) <mvmax4-costminigrid-dieselgeneratoreffectivehoursofoperationperyear>`                                                                      mg_dg_efhr     hours per year                    
:ref:`system (mini-grid) > diesel generator hours of operation per year (minimum) <mvmax4-costminigrid-dieselgeneratorminimumhoursofoperationperyear>`                                                                          mg_dg_mnhr     hours per year                    
:ref:`system (mini-grid) > diesel generator installation cost <mvmax4-costminigrid-dieselgeneratorinstallationcost>`                                                                                                            mg_dg_i        dollars                           
:ref:`system (mini-grid) > diesel generator installation cost as fraction of generator cost <mvmax4-costminigrid-dieselgeneratorinstallationcostasfractionofgeneratorcost>`                                                     mg_dg_if                                         
:ref:`system (mini-grid) > diesel generator lifetime <mvmax4-costminigrid-dieselgeneratorlifetime>`                                                                                                                             mg_dg_life     years                             
:ref:`system (mini-grid) > diesel generator operations and maintenance cost per year <mvmax4-costminigrid-dieselgeneratoroperationsandmaintenancecostperyear>`                                                                  mg_dg_om       dollars per year                  
:ref:`system (mini-grid) > diesel generator operations and maintenance cost per year as fraction of generator cost <mvmax4-costminigrid-dieselgeneratoroperationsandmaintenancecostperyearasfractionofgeneratorcost>`           mg_dg_omf                                        
:ref:`system (mini-grid) > diesel generator replacement cost per year <mvmax4-costminigrid-dieselgeneratorreplacementcostperyear>`                                                                                              mg_dg_rep      dollars per year                  
:ref:`system (mini-grid) > distribution loss <mvmax4-costminigrid-distributionloss>`                                                                                                                                            mg_loss        fraction                          
:ref:`system (mini-grid) > low voltage line equipment cost <mvmax4-costminigrid-lowvoltagelineequipmentcost>`                                                                                                                   mg_le          dollars                           
:ref:`system (mini-grid) > low voltage line equipment operations and maintenance cost per year <mvmax4-costminigrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear>`                                                mg_le_om       dollars per year                  
:ref:`system (mini-grid) > system initial cost <mvmax4-costminigrid-minigridsysteminitialcost>`                                                                                                                                 mg_ini         dollars                           
:ref:`system (mini-grid) > system nodal discounted cost <mvmax4-costminigrid-minigridsystemnodaldiscountedcost>`                                                                                                                mg_nod_d       dollars                           
:ref:`system (mini-grid) > system nodal levelized cost <mvmax4-costminigrid-minigridsystemnodallevelizedcost>`                                                                                                                  mg_nod_lev     dollars per kilowatt-hour         
:ref:`system (mini-grid) > system recurring cost per year <mvmax4-costminigrid-minigridsystemrecurringcostperyear>`                                                                                                             mg_rec         dollars per year                  
:ref:`system (mini-grid) > system total <mvmax4-minigridsystemtotal>`                                                                                                                                                           mg_ct          count                             
:ref:`system (mini-grid) > system total discounted cost <mvmax4-minigridsystemtotaldiscountedcost>`                                                                                                                             mg_tot_d       dollars                           
:ref:`system (mini-grid) > system total discounted demand <mvmax4-minigridsystemtotaldiscounteddemand>`                                                                                                                         mg_dem_d       kilowatt-hours                    
:ref:`system (mini-grid) > system total discounted diesel fuel cost <mvmax4-minigridsystemtotaldiscounteddieselfuelcost>`                                                                                                       mg_tot_ddfc    dollars                           
:ref:`system (mini-grid) > system total discounted recurring cost <mvmax4-minigridsystemtotaldiscountedrecurringcost>`                                                                                                          mg_tot_drc     dollars                           
:ref:`system (mini-grid) > system total initial cost <mvmax4-minigridsystemtotalinitialcost>`                                                                                                                                   mg_tot_i       dollars                           
:ref:`system (mini-grid) > system total levelized cost <mvmax4-minigridsystemtotallevelizedcost>`                                                                                                                               mg_tot_lev     dollars per kilowatt-hour         
:ref:`system (grid) > available system capacities (transformer) <mvmax4-costgrid-gridtransformeravailablesystemcapacities>`                                                                                                     gr_tr_cps      kilowatts list                    
:ref:`system (grid) > distribution loss <mvmax4-costgrid-distributionloss>`                                                                                                                                                     gr_loss        fraction                          
:ref:`system (grid) > electricity cost per kilowatt-hour <mvmax4-costgrid-gridelectricitycostperkilowatthour>`                                                                                                                  gr_el_ckwh     dollars per kilowatt-hour         
:ref:`system (grid) > electricity cost per year <mvmax4-costgrid-gridelectricitycostperyear>`                                                                                                                                   gr_el          dollars per year                  
:ref:`system (grid) > external nodal discounted cost per meter <mvmax4-costgrid-gridexternalsystemnodaldiscountedcostpermeter>`                                                                                                 ge_nodm_d      dollars per meter                 
:ref:`system (grid) > external nodal discounted recurring cost per meter <mvmax4-costgrid-gridexternalsystemnodaldiscountedrecurringcostpermeter>`                                                                              ge_nodm_drcpm  dollars per meter                 
:ref:`system (grid) > external system initial cost per meter <mvmax4-costgrid-gridexternalsysteminitialcostpermeter>`                                                                                                           ge_inim        dollars per meter                 
:ref:`system (grid) > external system recurring cost per meter per year <mvmax4-costgrid-gridexternalsystemrecurringcostpermeterperyear>`                                                                                       ge_recm        dollars per meter per year        
:ref:`system (grid) > grid transformer actual system capacity <mvmax4-costgrid-gridtransformeractualsystemcapacity>`                                                                                                            gr_tr_acp      kilowatts                         
:ref:`system (grid) > grid transformer actual system capacity counts <mvmax4-costgrid-gridtransformeractualsystemcapacitycounts>`                                                                                               gr_tr_acps     capacity count list               
:ref:`system (grid) > grid transformer desired system capacity <mvmax4-costgrid-gridtransformerdesiredsystemcapacity>`                                                                                                          gr_tr_dcp      kilowatts                         
:ref:`system (grid) > installation cost <mvmax4-costgrid-gridinstallationcost>`                                                                                                                                                 gr_i           dollars                           
:ref:`system (grid) > installation cost per connection <mvmax4-costgrid-gridinstallationcostperconnection>`                                                                                                                     gr_i_cc        dollars per connection            
:ref:`system (grid) > internal connection count <mvmax4-costgrid-gridinternalconnectioncount>`                                                                                                                                  gr_ic          connection count                  
:ref:`system (grid) > internal system initial cost <mvmax4-costgrid-gridinternalsysteminitialcost>`                                                                                                                             gi_ini         dollars                           
:ref:`system (grid) > internal system nodal discounted cost <mvmax4-costgrid-gridinternalsystemnodaldiscountedcost>`                                                                                                            gi_nod_d       dollars                           
:ref:`system (grid) > internal system nodal levelized cost <mvmax4-costgrid-gridinternalsystemnodallevelizedcost>`                                                                                                              gi_nod_lev     dollars per kilowatt-hour         
:ref:`system (grid) > internal system recurring cost per year <mvmax4-costgrid-gridinternalsystemrecurringcostperyear>`                                                                                                         gi_rec         dollars per year                  
:ref:`system (grid) > low voltage line equipment cost <mvmax4-costgrid-lowvoltagelineequipmentcost>`                                                                                                                            gr_le          dollars                           
:ref:`system (grid) > low voltage line equipment operations and maintenance cost per year <mvmax4-costgrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear>`                                                         gr_le_om       dollars per year                  
:ref:`system (grid) > medium voltage line cost per meter <mvmax4-costgrid-gridmediumvoltagelinecostpermeter>`                                                                                                                   gr_ml_cm       dollars per meter                 
:ref:`system (grid) > medium voltage line lifetime <mvmax4-costgrid-gridmediumvoltagelinelifetime>`                                                                                                                             gr_ml_life     years                             
:ref:`system (grid) > medium voltage line operations and maintenace cost per meter per year <mvmax4-costgrid-gridmediumvoltagelineoperationsandmaintenancecostpermeterperyear>`                                                 gr_ml_omm      dollars per meter per year        
:ref:`system (grid) > medium voltage line operations and maintenance cost per year as fraction of line cost <mvmax4-costgrid-gridmediumvoltagelineoperationsandmaintenancecostperyearasfractionoflinecost>`                     gr_ml_omf                                        
:ref:`system (grid) > medium voltage line replacement cost per meter per year <mvmax4-costgrid-gridmediumvoltagelinereplacementcostpermeterperyear>`                                                                            gr_ml_repm     dollars per meter per year        
:ref:`system (grid) > social infrastructure count <mvmax4-costgrid-gridsocialinfrastructurecount>`                                                                                                                              gr_so          facility count                    
:ref:`system (grid) > system total <mvmax4-gridsystemtotal>`                                                                                                                                                                    g_ct           count                             
:ref:`system (grid) > system total discounted cost <mvmax4-gridsystemtotaldiscountedcost>`                                                                                                                                      gr_tot_d       dollars                           
:ref:`system (grid) > system total discounted demand <mvmax4-gridsystemtotaldiscounteddemand>`                                                                                                                                  gr_dem_d       kilowatt-hours                    
:ref:`system (grid) > system total discounted recurring cost <mvmax4-gridsystemtotaldiscountedrecurringcost>`                                                                                                                   gr_tot_drc     dollars                           
:ref:`system (grid) > system total existing network length <mvmax4-gridsystemtotalexistingnetworklength>`                                                                                                                       gr_tot_enl     meters                            
:ref:`system (grid) > system total external discounted recurring cost <mvmax4-gridsystemtotalexternaldiscountedrecurringcost>`                                                                                                  gr_tot_ext_drc dollars                           
:ref:`system (grid) > system total external initial cost <mvmax4-gridsystemtotalexternalinitialcost>`                                                                                                                           gr_tot_ext_ic  dollars                           
:ref:`system (grid) > system total initial cost <mvmax4-gridsystemtotalinitialcost>`                                                                                                                                            gr_tot_init    dollars                           
:ref:`system (grid) > system total internal discounted recurring cost <mvmax4-gridsystemtotalinternaldiscountedrecurringcost>`                                                                                                  gr_tot_idrc    dollars                           
:ref:`system (grid) > system total internal initial cost <mvmax4-gridsystemtotalinternalinitialcost>`                                                                                                                           gr_tot_iic     dollars                           
:ref:`system (grid) > system total levelized cost <mvmax4-gridsystemtotallevelizedcost>`                                                                                                                                        gr_tot_lev     dollars per kilowatt-hour         
:ref:`system (grid) > system total proposed network length <mvmax4-gridsystemtotalproposednetworklength>`                                                                                                                       gr_tot_pnl     meters                            
:ref:`system (grid) > transformer cost <mvmax4-costgrid-gridtransformercost>`                                                                                                                                                   gr_tr          dollars                           
:ref:`system (grid) > transformer cost per grid system kilowatt <mvmax4-costgrid-gridtransformercostpergridsystemkilowatt>`                                                                                                     gr_tr_ckw      dollars per kilowatt              
:ref:`system (grid) > transformer lifetime <mvmax4-costgrid-gridtransformerlifetime>`                                                                                                                                           gr_tr_life     years                             
:ref:`system (grid) > transformer operations and maintenance cost per year <mvmax4-costgrid-gridtransformeroperationsandmaintenancecostperyear>`                                                                                gr_tr_om       dollars per year                  
:ref:`system (grid) > transformer operations and maintenance cost per year as fraction of transformer cost <mvmax4-costgrid-gridtransformeroperationsandmaintenancecostperyearasfractionoftransformercost>`                     gr_tr_omf                                        
:ref:`system (grid) > transformer replacement cost per year <mvmax4-costgrid-gridtransformerreplacementcostperyear>`                                                                                                            gr_tr_rep      dollars per year                  
:ref:`metric > maximum length of medium voltage line extension <mvmax4-metric>`                                                                                                                                                 mvmax          meters                            
:ref:`metric > system <mvmax4-system>`                                                                                                                                                                                          system                                           
=============================================================================================================================================================================================================================== ============== ==================================

Finance
-------

.. _mvmax4-finance-discountedcashflowfactor:

Discounted cash flow factor
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`finance > time horizon <mvmax4-finance-timehorizon>`

- :ref:`finance > interest rate per year <mvmax4-finance-interestrateperyear>`

Derivatives

- :ref:`system (grid) > external nodal discounted recurring cost per meter <mvmax4-costgrid-gridexternalsystemnodaldiscountedrecurringcostpermeter>`

- :ref:`system (grid) > internal system nodal discounted cost <mvmax4-costgrid-gridinternalsystemnodaldiscountedcost>`

- :ref:`system (mini-grid) > system nodal discounted cost <mvmax4-costminigrid-minigridsystemnodaldiscountedcost>`

- :ref:`system (off-grid) > system nodal discounted cost <mvmax4-costoffgrid-offgridsystemnodaldiscountedcost>`

- :ref:`demand > projected nodal discounted demand <mvmax4-demand-projectednodaldiscounteddemand>`


::

    class DiscountedCashFlowFactor(V):
    
        section = 'finance'
        option = 'discounted cash flow factor'
        aliases = ['dcff']
        dependencies = [
            TimeHorizon,
            InterestRatePerYear,
        ]
    
        def compute(self):
            interestExponents = [-x for x in xrange(1, self.get(TimeHorizon) + 1)]
            return sum(numpy.array(1 + self.get(InterestRatePerYear)) ** interestExponents)



.. _mvmax4-finance-economicgrowthrateperyear:

Economic growth rate per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`finance > electricity demand growth rate per year <mvmax4-finance-electricitydemandgrowthrateperyear>`


::

    class EconomicGrowthRatePerYear(V):
    
        section = 'finance'
        option = 'economic growth rate per year'
        aliases = ['economic_g']
        default = 0.06
        units = 'fraction per year'



.. _mvmax4-finance-elasticityofelectricitydemand:

Elasticity of electricity demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`finance > electricity demand growth rate per year <mvmax4-finance-electricitydemandgrowthrateperyear>`


::

    class ElasticityOfElectricityDemand(V):
    
        section = 'finance'
        option = 'elasticity of electricity demand'
        aliases = ['elasticity']
        default = 1.5



.. _mvmax4-finance-electricitydemandgrowthrateperyear:

Electricity demand growth rate per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`finance > elasticity of electricity demand <mvmax4-finance-elasticityofelectricitydemand>`

- :ref:`finance > economic growth rate per year <mvmax4-finance-economicgrowthrateperyear>`

Derivatives

- :ref:`finance > electricity demand multiplier <mvmax4-finance-electricitydemandmultiplier>`


::

    class ElectricityDemandGrowthRatePerYear(V):
    
        section = 'finance'
        option = 'electricity demand growth rate per year'
        aliases = ['dem_g']
        dependencies = [
            ElasticityOfElectricityDemand,
            EconomicGrowthRatePerYear,
        ]
        units = 'fraction per year'
    
        def compute(self):
            return abs(self.get(ElasticityOfElectricityDemand)) * self.get(EconomicGrowthRatePerYear)



.. _mvmax4-finance-electricitydemandmultiplier:

Electricity demand multiplier
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`finance > electricity demand growth rate per year <mvmax4-finance-electricitydemandgrowthrateperyear>`

- :ref:`finance > time horizon <mvmax4-finance-timehorizon>`

Derivatives

- :ref:`demand (social infrastructure) > projected commercial facility demand per year <mvmax4-demand-projectedcommercialfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected education facility demand per year <mvmax4-demand-projectededucationfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected health facility demand per year <mvmax4-demand-projectedhealthfacilitydemandperyear>`

- :ref:`demand (household) > projected household demand per year <mvmax4-demand-projectedhouseholddemandperyear>`

- :ref:`demand (productive) > projected productive demand <mvmax4-demand-projectedproductivedemandperyear>`

- :ref:`demand (social infrastructure) > projected public lighting facility demand per year <mvmax4-demand-projectedpubliclightingfacilitydemandperyear>`


::

    class ElectricityDemandMultiplier(V):
    
        section = 'finance'
        option = 'electricity demand multiplier'
        aliases = ['demf']
        dependencies = [
            ElectricityDemandGrowthRatePerYear,
            TimeHorizon,
        ]
    
        def compute(self):
            return (1 + self.get(ElectricityDemandGrowthRatePerYear)) ** self.get(TimeHorizon)



.. _mvmax4-finance-interestrateperyear:

Interest rate per year
^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`finance > discounted cash flow factor <mvmax4-finance-discountedcashflowfactor>`


::

    class InterestRatePerYear(V):
    
        section = 'finance'
        option = 'interest rate per year'
        aliases = ['interest_g']
        default = 0.1
        units = 'fraction per year'



.. _mvmax4-finance-timehorizon:

Time horizon
^^^^^^^^^^^^

Derivatives

- :ref:`finance > discounted cash flow factor <mvmax4-finance-discountedcashflowfactor>`

- :ref:`finance > electricity demand multiplier <mvmax4-finance-electricitydemandmultiplier>`

- :ref:`demographics > projected population counts <mvmax4-demographics-projectedpopulationcounts>`


::

    class TimeHorizon(V):
        
        section = 'finance'
        option = 'time horizon'
        aliases = ['time']
        c = dict(parse=store.parseCeilInteger)
        default = 10
        units = 'years'



Demographics
------------

.. _mvmax4-demographics-isrural:

Is rural
^^^^^^^^

Dependencies

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

- :ref:`demographics > urban population threshold <mvmax4-demographics-urbanpopulationthreshold>`

Derivatives

- :ref:`demographics > mean household size <mvmax4-demographics-meanhouseholdsize>`

- :ref:`demand (peak) > peak demand as fraction of nodal demand occurring during peak hours <mvmax4-demand-peakdemandasfractionofnodaldemandoccurringduringpeakhours>`


::

    class IsRural(V):
    
        section = 'demographics'
        option = 'is rural'
        aliases = ['rural']
        c = dict(parse=int)
        dependencies = [
            ProjectedPopulationCount,
            UrbanPopulationThreshold,
        ]
        units = 'binary'
    
        def compute(self):
            return 1 if self.get(ProjectedPopulationCount) < self.get(UrbanPopulationThreshold) else 0



.. _mvmax4-demographics-meanhouseholdsize:

Mean household size
^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demographics > mean household size (rural) <mvmax4-demographics-ruralmeanhouseholdsize>`

- :ref:`demographics > is rural <mvmax4-demographics-isrural>`

- :ref:`demographics > mean household size (urban) <mvmax4-demographics-urbanmeanhouseholdsize>`

Derivatives

- :ref:`demographics > projected household count <mvmax4-demographics-projectedhouseholdcount>`


::

    class MeanHouseholdSize(V):
    
        section = 'demographics'
        option = 'mean household size'
        aliases = ['ho_size']
        c = dict(check=store.assertPositive)
        dependencies = [
            RuralMeanHouseholdSize,
            IsRural,
            UrbanMeanHouseholdSize,
        ]
        units = 'person count'
    
        def compute(self):
            return self.get(RuralMeanHouseholdSize) if self.get(IsRural) else self.get(UrbanMeanHouseholdSize)



.. _mvmax4-demographics-meaninterhouseholddistance:

Mean interhousehold distance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`distribution > low voltage line length <mvmax4-costdistribution-lowvoltagelinelength>`


::

    class MeanInterhouseholdDistance(V):
    
        section = 'demographics'
        option = 'mean interhousehold distance'
        aliases = ['mid']
        default = 25
        units = 'meters'



.. _mvmax4-demographics-populationcount:

Population count
^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demographics > projected population counts <mvmax4-demographics-projectedpopulationcounts>`


::

    class PopulationCount(V):
    
        section = 'demographics'
        option = 'population count'
        aliases = ['pop', 'population']
        c = dict(parse=store.parseCeilInteger)
        default = 0
        units = 'person count'



.. _mvmax4-demographics-projectedhouseholdcount:

Projected household count
^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

- :ref:`demographics > mean household size <mvmax4-demographics-meanhouseholdsize>`

Derivatives

- :ref:`demand (household) > target household count <mvmax4-demand-targethouseholdcount>`


::

    class ProjectedHouseholdCount(V):
    
        section = 'demographics'
        option = 'projected household count'
        aliases = ['p_ho']
        c = dict(check=store.assertNonNegative)
        dependencies = [
            ProjectedPopulationCount,
            MeanHouseholdSize,
        ]
        units = 'household count'
    
        def compute(self):
            return math.ceil(self.get(ProjectedPopulationCount) / float(self.get(MeanHouseholdSize)))



.. _mvmax4-demographics-projectedpopulationcount:

Projected population count
^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demographics > projected population counts <mvmax4-demographics-projectedpopulationcounts>`

Derivatives

- :ref:`demographics > is rural <mvmax4-demographics-isrural>`

- :ref:`demand (social infrastructure) > projected commercial facility count <mvmax4-demand-projectedcommercialfacilitycount>`

- :ref:`demand (social infrastructure) > projected commercial facility demand per year <mvmax4-demand-projectedcommercialfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected education facility count <mvmax4-demand-projectededucationfacilitycount>`

- :ref:`demand (social infrastructure) > projected education facility demand per year <mvmax4-demand-projectededucationfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected health facility count <mvmax4-demand-projectedhealthfacilitycount>`

- :ref:`demand (social infrastructure) > projected health facility demand per year <mvmax4-demand-projectedhealthfacilitydemandperyear>`

- :ref:`demographics > projected household count <mvmax4-demographics-projectedhouseholdcount>`

- :ref:`demand (household) > projected household demand per year <mvmax4-demand-projectedhouseholddemandperyear>`

- :ref:`demand (productive) > projected productive demand <mvmax4-demand-projectedproductivedemandperyear>`

- :ref:`demand (social infrastructure) > projected public lighting facility count <mvmax4-demand-projectedpubliclightingfacilitycount>`

- :ref:`demand (social infrastructure) > projected public lighting facility demand per year <mvmax4-demand-projectedpubliclightingfacilitydemandperyear>`


::

    class ProjectedPopulationCount(V):
    
        section = 'demographics'
        option = 'projected population count'
        aliases = ['p_pop']
        c = dict(parse=store.parseCeilInteger)
        dependencies = [
            ProjectedPopulationCounts,
        ]
        units = 'person count'
    
        def compute(self):
            return self.get(ProjectedPopulationCounts)[-1]



.. _mvmax4-demographics-projectedpopulationcounts:

Projected population counts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demographics > population count <mvmax4-demographics-populationcount>`

- :ref:`demographics > population growth rate per year (rural) <mvmax4-demographics-ruralpopulationgrowthrateperyear>`

- :ref:`demographics > population growth rate per year (urban) <mvmax4-demographics-urbanpopulationgrowthrateperyear>`

- :ref:`demographics > urban population threshold <mvmax4-demographics-urbanpopulationthreshold>`

- :ref:`finance > time horizon <mvmax4-finance-timehorizon>`

Derivatives

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`


::

    class ProjectedPopulationCounts(V):
    
        section = 'demographics'
        option = 'projected population counts'
        aliases = ['p_pops']
        c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
        dependencies = [
            PopulationCount,
            RuralPopulationGrowthRatePerYear,
            UrbanPopulationGrowthRatePerYear,
            UrbanPopulationThreshold,
            finance.TimeHorizon,
        ]
        units = 'person count list'
    
        def compute(self):
            # Initialize
            populationCounts = [self.get(PopulationCount)]
            urbanThreshold = self.get(UrbanPopulationThreshold)
            ruralGrowthRate = self.get(RuralPopulationGrowthRatePerYear)
            urbanGrowthRate = self.get(UrbanPopulationGrowthRatePerYear)
            # For each year of the time horizon,
            for year in xrange(self.get(finance.TimeHorizon)):
                # Get population count
                populationCount = populationCounts[-1]
                # Get appropriate growth rate
                populationGrowthRate = ruralGrowthRate if populationCount < urbanThreshold else urbanGrowthRate
                # Append projected population count
                populationCounts.append(int(math.ceil(populationCount * (1 + populationGrowthRate))))
            # Return
            return populationCounts



.. _mvmax4-demographics-ruralmeanhouseholdsize:

Rural mean household size
^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demographics > mean household size <mvmax4-demographics-meanhouseholdsize>`


::

    class RuralMeanHouseholdSize(V):
    
        section = 'demographics'
        option = 'mean household size (rural)'
        aliases = ['ho_size_r']
        default = 9.6
        units = 'person count'



.. _mvmax4-demographics-ruralpopulationgrowthrateperyear:

Rural population growth rate per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demographics > projected population counts <mvmax4-demographics-projectedpopulationcounts>`


::

    class RuralPopulationGrowthRatePerYear(V):
    
        section = 'demographics'
        option = 'population growth rate per year (rural)'
        aliases = ['pop_g_r']
        default = 0.015
        units = 'fraction per year'



.. _mvmax4-demographics-urbanmeanhouseholdsize:

Urban mean household size
^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demographics > mean household size <mvmax4-demographics-meanhouseholdsize>`


::

    class UrbanMeanHouseholdSize(V):
    
        section = 'demographics'
        option = 'mean household size (urban)'
        aliases = ['ho_size_u']
        default = 7.5
        units = 'person count'



.. _mvmax4-demographics-urbanpopulationgrowthrateperyear:

Urban population growth rate per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demographics > projected population counts <mvmax4-demographics-projectedpopulationcounts>`


::

    class UrbanPopulationGrowthRatePerYear(V):
    
        section = 'demographics'
        option = 'population growth rate per year (urban)'
        aliases = ['pop_g_u']
        default = 0.036
        units = 'fraction per year'



.. _mvmax4-demographics-urbanpopulationthreshold:

Urban population threshold
^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demographics > is rural <mvmax4-demographics-isrural>`

- :ref:`demographics > projected population counts <mvmax4-demographics-projectedpopulationcounts>`


::

    class UrbanPopulationThreshold(V):
    
        section = 'demographics'
        option = 'urban population threshold'
        aliases = ['u_pop_thre']
        c = dict(parse=store.parseCeilInteger)
        default = 5000
        units = 'person count'



Demand
------

.. _mvmax4-demand-projectednodaldemandperyear:

Projected nodal demand per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (household) > projected household demand per year <mvmax4-demand-projectedhouseholddemandperyear>`

- :ref:`demand (productive) > projected productive demand <mvmax4-demand-projectedproductivedemandperyear>`

- :ref:`demand (social infrastructure) > projected health facility demand per year <mvmax4-demand-projectedhealthfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected education facility demand per year <mvmax4-demand-projectededucationfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected commercial facility demand per year <mvmax4-demand-projectedcommercialfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected public lighting facility demand per year <mvmax4-demand-projectedpubliclightingfacilitydemandperyear>`

Derivatives

- :ref:`system (mini-grid) > diesel generator hours of operation per year (effective) <mvmax4-costminigrid-dieselgeneratoreffectivehoursofoperationperyear>`

- :ref:`system (grid) > electricity cost per year <mvmax4-costgrid-gridelectricitycostperyear>`

- :ref:`system (grid) > internal system nodal discounted cost <mvmax4-costgrid-gridinternalsystemnodaldiscountedcost>`

- :ref:`system (mini-grid) > system nodal discounted cost <mvmax4-costminigrid-minigridsystemnodaldiscountedcost>`

- :ref:`system (off-grid) > system nodal discounted cost <mvmax4-costoffgrid-offgridsystemnodaldiscountedcost>`

- :ref:`demand > projected nodal discounted demand <mvmax4-demand-projectednodaldiscounteddemand>`

- :ref:`demand (peak) > projected peak nodal demand <mvmax4-demand-projectedpeaknodaldemand>`

- :ref:`metric > system <mvmax4-system>`


::

    class ProjectedNodalDemandPerYear(V):
    
        section = 'demand'
        option = 'projected nodal demand per year'
        aliases = ['p_dem']
        dependencies = [
            ProjectedHouseholdDemandPerYear,
            ProjectedProductiveDemandPerYear,
            ProjectedHealthFacilityDemandPerYear,
            ProjectedEducationFacilityDemandPerYear,
            ProjectedCommercialFacilityDemandPerYear,
            ProjectedPublicLightingFacilityDemandPerYear,
        ]
        units = 'kilowatt-hours per year'
    
        def compute(self):
            return sum([
                self.get(ProjectedHouseholdDemandPerYear),
                self.get(ProjectedProductiveDemandPerYear),
                self.get(ProjectedHealthFacilityDemandPerYear),
                self.get(ProjectedEducationFacilityDemandPerYear),
                self.get(ProjectedCommercialFacilityDemandPerYear),
                self.get(ProjectedPublicLightingFacilityDemandPerYear),
            ])



.. _mvmax4-demand-projectednodaldiscounteddemand:

Projected nodal discounted demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`finance > discounted cash flow factor <mvmax4-finance-discountedcashflowfactor>`

Derivatives

- :ref:`system (grid) > internal system nodal levelized cost <mvmax4-costgrid-gridinternalsystemnodallevelizedcost>`

- :ref:`system (mini-grid) > system nodal levelized cost <mvmax4-costminigrid-minigridsystemnodallevelizedcost>`

- :ref:`system (off-grid) > system nodal levelized cost <mvmax4-costoffgrid-offgridsystemnodallevelizedcost>`


::

    class ProjectedNodalDiscountedDemand(V):
        """
        Note that we are overestimating nodal demand aggregated over the time horizon
        since we are using the projected demand at the end of the time horizon as the
        recurring demand per year, which in real-life should scale year by year.
        """
    
        section = 'demand'
        option = 'projected nodal discounted demand'
        aliases = ['p_dem_d']
        dependencies = [
            ProjectedNodalDemandPerYear,
            finance.DiscountedCashFlowFactor,
        ]
        units = 'kilowatt-hours'
    
        def compute(self):
            return self.get(ProjectedNodalDemandPerYear) * self.get(finance.DiscountedCashFlowFactor)



Demand (peak)
-------------

.. _mvmax4-demand-demandtopeakdemandconversionfactor:

Demand to peak demand conversion factor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (peak) > peak demand as fraction of nodal demand occurring during peak hours <mvmax4-demand-peakdemandasfractionofnodaldemandoccurringduringpeakhours>`

- :ref:`demand (peak) > peak electrical hours of operation per year <mvmax4-demand-peakelectricalhoursofoperationperyear>`

Derivatives

- :ref:`demand (peak) > projected peak commercial facility demand <mvmax4-demand-projectedpeakcommercialfacilitydemand>`

- :ref:`demand (peak) > projected peak nodal demand <mvmax4-demand-projectedpeaknodaldemand>`

- :ref:`demand (peak) > projected peak productive demand <mvmax4-demand-projectedpeakproductivedemand>`


::

    class DemandToPeakDemandConversionFactor(V):
    
        section = 'demand (peak)'
        option = 'demand to peak demand conversion factor'
        aliases = ['dem_pkdemf']
        dependencies = [
            PeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours,
            PeakElectricalHoursOfOperationPerYear,
        ]
    
        def compute(self):
            return self.get(PeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours) / float(self.get(PeakElectricalHoursOfOperationPerYear))



.. _mvmax4-demand-peakdemandasfractionofnodaldemandoccurringduringpeakhours:

Peak demand as fraction of nodal demand occurring during peak hours
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (peak) > peak demand as fraction of nodal demand occurring during peak hours (rural) <mvmax4-demand-ruralpeakdemandasfractionofnodaldemandoccurringduringpeakhours>`

- :ref:`demographics > is rural <mvmax4-demographics-isrural>`

- :ref:`demand (peak) > peak demand as fraction of nodal demand occurring during peak hours (urban) <mvmax4-demand-urbanpeakdemandasfractionofnodaldemandoccurringduringpeakhours>`

Derivatives

- :ref:`demand (peak) > demand to peak demand conversion factor <mvmax4-demand-demandtopeakdemandconversionfactor>`


::

    class PeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours(V):
    
        section = 'demand (peak)'
        option = 'peak demand as fraction of nodal demand occurring during peak hours'
        aliases = ['pkdemf']
        dependencies = [
            RuralPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours,
            demographics.IsRural,
            UrbanPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours,
        ]
    
        def compute(self):
            return self.get(RuralPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours) if self.get(demographics.IsRural) else self.get(UrbanPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours)



.. _mvmax4-demand-peakelectricalhoursofoperationperyear:

Peak electrical hours of operation per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (peak) > demand to peak demand conversion factor <mvmax4-demand-demandtopeakdemandconversionfactor>`


::

    class PeakElectricalHoursOfOperationPerYear(V):
    
        section = 'demand (peak)'
        option = 'peak electrical hours of operation per year'
        aliases = ['pkel_hr']
        c = dict(check=store.assertPositive)
        default = 1460
        units = 'hours per year'



.. _mvmax4-demand-projectedpeakcommercialfacilitydemand:

Projected peak commercial facility demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > projected commercial facility demand per year <mvmax4-demand-projectedcommercialfacilitydemandperyear>`

- :ref:`demand (peak) > demand to peak demand conversion factor <mvmax4-demand-demandtopeakdemandconversionfactor>`

Derivatives

- :ref:`system (off-grid) > diesel generator desired system capacity <mvmax4-costoffgrid-dieselgeneratordesiredsystemcapacity>`


::

    class ProjectedPeakCommercialFacilityDemand(V):
    
        section = 'demand (peak)'
        option = 'projected peak commercial facility demand'
        aliases = ['p_pkdem_co']
        dependencies = [
            ProjectedCommercialFacilityDemandPerYear,
            DemandToPeakDemandConversionFactor,
        ]
        units = 'kilowatts'
    
        def compute(self):
            return self.get(ProjectedCommercialFacilityDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)



.. _mvmax4-demand-projectedpeaknodaldemand:

Projected peak nodal demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`demand (peak) > demand to peak demand conversion factor <mvmax4-demand-demandtopeakdemandconversionfactor>`

Derivatives

- :ref:`system (mini-grid) > diesel generator desired system capacity <mvmax4-costminigrid-dieselgeneratordesiredsystemcapacity>`

- :ref:`system (grid) > grid transformer desired system capacity <mvmax4-costgrid-gridtransformerdesiredsystemcapacity>`


::

    class ProjectedPeakNodalDemand(V):
    
        section = 'demand (peak)'
        option = 'projected peak nodal demand'
        aliases = ['p_pkdem']
        dependencies = [
            ProjectedNodalDemandPerYear,
            DemandToPeakDemandConversionFactor,
        ]
        units = 'kilowatts'
    
        def compute(self):
            return self.get(ProjectedNodalDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)



.. _mvmax4-demand-projectedpeakproductivedemand:

Projected peak productive demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (productive) > projected productive demand <mvmax4-demand-projectedproductivedemandperyear>`

- :ref:`demand (peak) > demand to peak demand conversion factor <mvmax4-demand-demandtopeakdemandconversionfactor>`

Derivatives

- :ref:`system (off-grid) > diesel generator desired system capacity <mvmax4-costoffgrid-dieselgeneratordesiredsystemcapacity>`


::

    class ProjectedPeakProductiveDemand(V):
    
        section = 'demand (peak)'
        option = 'projected peak productive demand'
        aliases = ['p_pkdem_pr']
        dependencies = [
            ProjectedProductiveDemandPerYear,
            DemandToPeakDemandConversionFactor,
        ]
        units = 'kilowatts'
    
        def compute(self):
            return self.get(ProjectedProductiveDemandPerYear) * self.get(DemandToPeakDemandConversionFactor)



.. _mvmax4-demand-ruralpeakdemandasfractionofnodaldemandoccurringduringpeakhours:

Rural peak demand as fraction of nodal demand occurring during peak hours
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (peak) > peak demand as fraction of nodal demand occurring during peak hours <mvmax4-demand-peakdemandasfractionofnodaldemandoccurringduringpeakhours>`


::

    class RuralPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours(V):
    
        section = 'demand (peak)'
        option = 'peak demand as fraction of nodal demand occurring during peak hours (rural)'
        aliases = ['pkdemf_r']
        default = 0.4



.. _mvmax4-demand-urbanpeakdemandasfractionofnodaldemandoccurringduringpeakhours:

Urban peak demand as fraction of nodal demand occurring during peak hours
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (peak) > peak demand as fraction of nodal demand occurring during peak hours <mvmax4-demand-peakdemandasfractionofnodaldemandoccurringduringpeakhours>`


::

    class UrbanPeakDemandAsFractionOfNodalDemandOccurringDuringPeakHours(V):
    
        section = 'demand (peak)'
        option = 'peak demand as fraction of nodal demand occurring during peak hours (urban)'
        aliases = ['pkdemf_u']
        default = 0.4



Demand (household)
------------------

.. _mvmax4-demand-householddemandcurve:

Household demand curve
^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (household) > demand curve type <mvmax4-demand-householddemandcurvetype>`

- :ref:`demand (household) > demand curve points (population and multiplier) <mvmax4-demand-householddemandcurvepoints>`

Derivatives

- :ref:`demand (household) > projected household demand per year <mvmax4-demand-projectedhouseholddemandperyear>`


::

    class HouseholdDemandCurve(V):
    
        section = 'demand (household)'
        option = 'demand curve'
        aliases = ['ho_dc']
        c = dict(parse=curve.parse, format=curve.format)
        dependencies = [
            HouseholdDemandCurveType,
            HouseholdDemandCurvePoints,
        ]
    
        def compute(self):
            curveType = self.get(HouseholdDemandCurveType)
            curvePoints = self.get(HouseholdDemandCurvePoints)
            return curve.fit(curveType, curvePoints)



.. _mvmax4-demand-householddemandcurvepoints:

Household demand curve points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (household) > demand curve <mvmax4-demand-householddemandcurve>`


::

    class HouseholdDemandCurvePoints(V):
    
        section = 'demand (household)'
        option = 'demand curve points (population and multiplier)'
        aliases = ['ho_dc_pts']
        c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
        default = '500 1; 1000 1.56; 5000 6.16; 10000 11.5'
        units = 'population and multiplier list'



.. _mvmax4-demand-householddemandcurvetype:

Household demand curve type
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (household) > demand curve <mvmax4-demand-householddemandcurve>`


::

    class HouseholdDemandCurveType(V):
    
        section = 'demand (household)'
        option = 'demand curve type'
        aliases = ['ho_dc_t']
        c = dict(parse=str, input=curve.inputCurveType)
        default = 'ZeroLogisticLinear'



.. _mvmax4-demand-householdunitdemandperhouseholdperyear:

Household unit demand per household per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (household) > projected household demand per year <mvmax4-demand-projectedhouseholddemandperyear>`


::

    class HouseholdUnitDemandPerHouseholdPerYear(V):
    
        section = 'demand (household)'
        option = 'household unit demand per household per year'
        aliases = ['ho_dc_unit']
        default = 0 # 100
        units = 'kilowatt-hours per year'



.. _mvmax4-demand-projectedhouseholddemandperyear:

Projected household demand per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`finance > electricity demand multiplier <mvmax4-finance-electricitydemandmultiplier>`

- :ref:`demand (household) > demand curve <mvmax4-demand-householddemandcurve>`

- :ref:`demand (household) > household unit demand per household per year <mvmax4-demand-householdunitdemandperhouseholdperyear>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

- :ref:`demand (household) > target household count <mvmax4-demand-targethouseholdcount>`

Derivatives

- :ref:`system (off-grid) > photovoltaic panel desired capacity <mvmax4-costoffgrid-photovoltaicpaneldesiredsystemcapacity>`

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`


::

    class ProjectedHouseholdDemandPerYear(V):
    
        section = 'demand (household)'
        option = 'projected household demand per year'
        aliases = ['p_dem_ho']
        dependencies = [
            finance.ElectricityDemandMultiplier,
            HouseholdDemandCurve,
            HouseholdUnitDemandPerHouseholdPerYear,
            demographics.ProjectedPopulationCount,
            TargetHouseholdCount,
        ]
        units = 'kilowatt-hours per year'
    
        def compute(self):
            return self.get(finance.ElectricityDemandMultiplier) * self.get(HouseholdDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(HouseholdUnitDemandPerHouseholdPerYear) * self.get(TargetHouseholdCount)



.. _mvmax4-demand-targethouseholdcount:

Target household count
^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (household) > target household penetration rate <mvmax4-demand-targethouseholdpenetrationrate>`

- :ref:`demographics > projected household count <mvmax4-demographics-projectedhouseholdcount>`

Derivatives

- :ref:`system (grid) > internal connection count <mvmax4-costgrid-gridinternalconnectioncount>`

- :ref:`system (mini-grid) > low voltage line equipment cost <mvmax4-costminigrid-lowvoltagelineequipmentcost>`

- :ref:`distribution > low voltage line length <mvmax4-costdistribution-lowvoltagelinelength>`

- :ref:`demand (household) > projected household demand per year <mvmax4-demand-projectedhouseholddemandperyear>`

- :ref:`demand (productive) > projected productive demand <mvmax4-demand-projectedproductivedemandperyear>`


::

    class TargetHouseholdCount(V):
    
        section = 'demand (household)'
        option = 'target household count'
        aliases = ['ct_hh_t']
        c = dict(parse=store.parseCeilInteger)
        dependencies = [
            TargetHouseholdPenetrationRate,
            demographics.ProjectedHouseholdCount,
        ]
        units = 'households'
    
        def compute(self):
            return math.ceil(self.get(TargetHouseholdPenetrationRate) * self.get(demographics.ProjectedHouseholdCount))



.. _mvmax4-demand-targethouseholdpenetrationrate:

Target household penetration rate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (household) > target household count <mvmax4-demand-targethouseholdcount>`


::

    class TargetHouseholdPenetrationRate(V):
    
        section = 'demand (household)'
        option = 'target household penetration rate'
        default = 1



Demand (productive)
-------------------

.. _mvmax4-demand-productivedemandcurve:

Productive demand curve
^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (productive) > demand curve type <mvmax4-demand-productivedemandcurvetype>`

- :ref:`demand (productive) > demand curve points (population and multiplier) <mvmax4-demand-productivedemandcurvepoints>`

Derivatives

- :ref:`demand (productive) > projected productive demand <mvmax4-demand-projectedproductivedemandperyear>`


::

    class ProductiveDemandCurve(V):
    
        section = 'demand (productive)'
        option = 'demand curve'
        aliases = ['pr_dc']
        c = dict(parse=curve.parse, format=curve.format)
        dependencies = [
            ProductiveDemandCurveType,
            ProductiveDemandCurvePoints,
        ]
    
        def compute(self):
            curveType = self.get(ProductiveDemandCurveType)
            curvePoints = self.get(ProductiveDemandCurvePoints)
            return curve.fit(curveType, curvePoints)



.. _mvmax4-demand-productivedemandcurvepoints:

Productive demand curve points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (productive) > demand curve <mvmax4-demand-productivedemandcurve>`


::

    class ProductiveDemandCurvePoints(V):
    
        section = 'demand (productive)'
        option = 'demand curve points (population and multiplier)'
        aliases = ['pr_dc_pts']
        c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
        default = '500 1; 1000 3.06; 5000 3.57; 10000 5.10'
        units = 'population and multiplier list'



.. _mvmax4-demand-productivedemandcurvetype:

Productive demand curve type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (productive) > demand curve <mvmax4-demand-productivedemandcurve>`


::

    class ProductiveDemandCurveType(V):
    
        section = 'demand (productive)'
        option = 'demand curve type'
        aliases = ['pr_dc_t']
        c = dict(parse=str, input=curve.inputCurveType)
        default = 'ZeroLogisticLinear'



.. _mvmax4-demand-productiveunitdemandperhouseholdperyear:

Productive unit demand per household per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (productive) > projected productive demand <mvmax4-demand-projectedproductivedemandperyear>`


::

    class ProductiveUnitDemandPerHouseholdPerYear(V):
    
        section = 'demand (productive)'
        option = 'productive unit demand per household per year'
        aliases = ['pr_dc_unit']
        default = 0 # 19.5
        units = 'kilowatt-hours per year'



.. _mvmax4-demand-projectedproductivedemandperyear:

Projected productive demand per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`finance > electricity demand multiplier <mvmax4-finance-electricitydemandmultiplier>`

- :ref:`demand (productive) > demand curve <mvmax4-demand-productivedemandcurve>`

- :ref:`demand (productive) > productive unit demand per household per year <mvmax4-demand-productiveunitdemandperhouseholdperyear>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

- :ref:`demand (household) > target household count <mvmax4-demand-targethouseholdcount>`

Derivatives

- :ref:`system (off-grid) > diesel generator hours of operation per year (effective) <mvmax4-costoffgrid-dieselgeneratoreffectivehoursofoperationperyear>`

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`demand (peak) > projected peak productive demand <mvmax4-demand-projectedpeakproductivedemand>`


::

    class ProjectedProductiveDemandPerYear(V):
        """
        Productive demand is power for community resources such as water pumps
        and grinding mills.  By estimating productive demand on a per household 
        basis, we do not have to estimate the number of water pumps or 
        grinding mills that are shared by a village.  The number of water pumps
        or grinding mills is generally smaller than the number of households.
        """
    
        section = 'demand (productive)'
        option = 'projected productive demand'
        aliases = ['p_dem_pr']
        dependencies = [
            finance.ElectricityDemandMultiplier,
            ProductiveDemandCurve,
            ProductiveUnitDemandPerHouseholdPerYear,
            demographics.ProjectedPopulationCount,
            TargetHouseholdCount,
        ]
        units = 'kilowatt-hours per year'
    
        def compute(self):
            return self.get(finance.ElectricityDemandMultiplier) * self.get(ProductiveDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(ProductiveUnitDemandPerHouseholdPerYear) * self.get(TargetHouseholdCount)



Demand (social infrastructure)
------------------------------

.. _mvmax4-demand-commercialfacilitycountcurve:

Commercial facility count curve
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > commercial facility count curve type <mvmax4-demand-commercialfacilitycountcurvetype>`

- :ref:`demand (social infrastructure) > commercial facility count curve points (population and facility count) <mvmax4-demand-commercialfacilitycountcurvepoints>`

Derivatives

- :ref:`demand (social infrastructure) > projected commercial facility count <mvmax4-demand-projectedcommercialfacilitycount>`


::

    class CommercialFacilityCountCurve(V):
    
        section = 'demand (social infrastructure)'
        option = 'commercial facility count curve'
        aliases = ['co_cc']
        c = dict(parse=curve.parse, format=curve.format)
        dependencies = [
            CommercialFacilityCountCurveType,
            CommercialFacilityCountCurvePoints,
        ]
    
        def compute(self):
            curveType = self.get(CommercialFacilityCountCurveType)
            curvePoints = self.get(CommercialFacilityCountCurvePoints)
            return curve.fit(curveType, curvePoints)



.. _mvmax4-demand-commercialfacilitycountcurvepoints:

Commercial facility count curve points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > commercial facility count curve <mvmax4-demand-commercialfacilitycountcurve>`


::

    class CommercialFacilityCountCurvePoints(V):
    
        section = 'demand (social infrastructure)'
        option = 'commercial facility count curve points (population and facility count)'
        aliases = ['co_cc_pts']
        c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
        default = '50 0.12; 500 1.2; 5000 25; 10000 125'
        units = 'population and facility count list'



.. _mvmax4-demand-commercialfacilitycountcurvetype:

Commercial facility count curve type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > commercial facility count curve <mvmax4-demand-commercialfacilitycountcurve>`


::

    class CommercialFacilityCountCurveType(V):
    
        section = 'demand (social infrastructure)'
        option = 'commercial facility count curve type'
        aliases = ['co_cc_t']
        c = dict(parse=str, input=curve.inputCurveType)
        default = 'ZeroLogisticLinear'



.. _mvmax4-demand-commercialfacilityunitdemandpercommercialfacilityperyear:

Commercial facility unit demand per commercial facility per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > projected commercial facility demand per year <mvmax4-demand-projectedcommercialfacilitydemandperyear>`


::

    class CommercialFacilityUnitDemandPerCommercialFacilityPerYear(V):
    
        section = 'demand (social infrastructure)'
        option = 'commercial facility unit demand per commercial facility per year'
        aliases = ['co_dc_unit']
        default = 0 # 250
        units = 'kilowatt-hours per year'



.. _mvmax4-demand-educationfacilitycountcurve:

Education facility count curve
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > education facility count curve type <mvmax4-demand-educationfacilitycountcurvetype>`

- :ref:`demand (social infrastructure) > education facility count curve points (population and facility count) <mvmax4-demand-educationfacilitycountcurvepoints>`

Derivatives

- :ref:`demand (social infrastructure) > projected education facility count <mvmax4-demand-projectededucationfacilitycount>`


::

    class EducationFacilityCountCurve(V):
    
        section = 'demand (social infrastructure)'
        option = 'education facility count curve'
        aliases = ['ed_cc']
        c = dict(parse=curve.parse, format=curve.format)
        dependencies = [
            EducationFacilityCountCurveType,
            EducationFacilityCountCurvePoints,
        ]
    
        def compute(self):
            curveType = self.get(EducationFacilityCountCurveType)
            curvePoints = self.get(EducationFacilityCountCurvePoints)
            return curve.fit(curveType, curvePoints)



.. _mvmax4-demand-educationfacilitycountcurvepoints:

Education facility count curve points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > education facility count curve <mvmax4-demand-educationfacilitycountcurve>`


::

    class EducationFacilityCountCurvePoints(V):
    
        section = 'demand (social infrastructure)'
        option = 'education facility count curve points (population and facility count)'
        aliases = ['ed_cc_pts']
        c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
        default = '50 0.1; 500 1; 5000 3; 10000 15'
        units = 'population and facility count list'



.. _mvmax4-demand-educationfacilitycountcurvetype:

Education facility count curve type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > education facility count curve <mvmax4-demand-educationfacilitycountcurve>`


::

    class EducationFacilityCountCurveType(V):
    
        section = 'demand (social infrastructure)'
        option = 'education facility count curve type'
        aliases = ['ed_cc_t']
        c = dict(parse=str, input=curve.inputCurveType)
        default = 'ZeroLogisticLinear'



.. _mvmax4-demand-educationfacilityunitdemandpereducationfacilityperyear:

Education facility unit demand per education facility per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > projected education facility demand per year <mvmax4-demand-projectededucationfacilitydemandperyear>`


::

    class EducationFacilityUnitDemandPerEducationFacilityPerYear(V):
    
        section = 'demand (social infrastructure)'
        option = 'education facility unit demand per education facility per year'
        aliases = ['ed_dc_unit']
        default = 0 # 1200
        units = 'kilowatt-hours per year'



.. _mvmax4-demand-healthfacilitycountcurve:

Health facility count curve
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > health facility count curve type <mvmax4-demand-healthfacilitycountcurvetype>`

- :ref:`demand (social infrastructure) > health facility count curve points (population and facility count) <mvmax4-demand-healthfacilitycountcurvepoints>`

Derivatives

- :ref:`demand (social infrastructure) > projected health facility count <mvmax4-demand-projectedhealthfacilitycount>`


::

    class HealthFacilityCountCurve(V):
    
        section = 'demand (social infrastructure)'
        option = 'health facility count curve'
        aliases = ['he_cc']
        c = dict(parse=curve.parse, format=curve.format)
        dependencies = [
            HealthFacilityCountCurveType,
            HealthFacilityCountCurvePoints,
        ]
    
        def compute(self):
            curveType = self.get(HealthFacilityCountCurveType)
            curvePoints = self.get(HealthFacilityCountCurvePoints)
            return curve.fit(curveType, curvePoints)



.. _mvmax4-demand-healthfacilitycountcurvepoints:

Health facility count curve points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > health facility count curve <mvmax4-demand-healthfacilitycountcurve>`


::

    class HealthFacilityCountCurvePoints(V):
    
        section = 'demand (social infrastructure)'
        option = 'health facility count curve points (population and facility count)'
        aliases = ['he_cc_pts']
        c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
        default = '50 0.16; 500 1.6; 5000 5; 10000 20'
        units = 'population and facility count list'



.. _mvmax4-demand-healthfacilitycountcurvetype:

Health facility count curve type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > health facility count curve <mvmax4-demand-healthfacilitycountcurve>`


::

    class HealthFacilityCountCurveType(V):
    
        section = 'demand (social infrastructure)'
        option = 'health facility count curve type'
        aliases = ['he_cc_t']
        c = dict(parse=str, input=curve.inputCurveType)
        default = 'ZeroLogisticLinear'



.. _mvmax4-demand-healthfacilityunitdemandperhealthfacilityperyear:

Health facility unit demand per health facility per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > projected health facility demand per year <mvmax4-demand-projectedhealthfacilitydemandperyear>`


::

    class HealthFacilityUnitDemandPerHealthFacilityPerYear(V):
    
        section = 'demand (social infrastructure)'
        option = 'health facility unit demand per health facility per year'
        aliases = ['he_dc_unit']
        default = 0 # 1000
        units = 'kilowatt-hours per year'



.. _mvmax4-demand-projectedcommercialfacilitycount:

Projected commercial facility count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > commercial facility count curve <mvmax4-demand-commercialfacilitycountcurve>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

Derivatives

- :ref:`system (grid) > social infrastructure count <mvmax4-costgrid-gridsocialinfrastructurecount>`

- :ref:`demand (social infrastructure) > projected commercial facility demand per year <mvmax4-demand-projectedcommercialfacilitydemandperyear>`


::

    class ProjectedCommercialFacilityCount(V):
    
        section = 'demand (social infrastructure)'
        option = 'projected commercial facility count'
        aliases = ['p_co']
        dependencies = [
            CommercialFacilityCountCurve,
            demographics.ProjectedPopulationCount,
        ]
        units = 'commercial facility count'
    
        def compute(self):
            return self.get(CommercialFacilityCountCurve).interpolate(self.get(demographics.ProjectedPopulationCount))



.. _mvmax4-demand-projectedcommercialfacilitydemandperyear:

Projected commercial facility demand per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`finance > electricity demand multiplier <mvmax4-finance-electricitydemandmultiplier>`

- :ref:`demand (social infrastructure) > demand curve <mvmax4-demand-socialinfrastructuredemandcurve>`

- :ref:`demand (social infrastructure) > commercial facility unit demand per commercial facility per year <mvmax4-demand-commercialfacilityunitdemandpercommercialfacilityperyear>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

- :ref:`demand (social infrastructure) > projected commercial facility count <mvmax4-demand-projectedcommercialfacilitycount>`

Derivatives

- :ref:`system (off-grid) > diesel generator hours of operation per year (effective) <mvmax4-costoffgrid-dieselgeneratoreffectivehoursofoperationperyear>`

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`demand (peak) > projected peak commercial facility demand <mvmax4-demand-projectedpeakcommercialfacilitydemand>`


::

    class ProjectedCommercialFacilityDemandPerYear(V):
    
        section = 'demand (social infrastructure)'
        option = 'projected commercial facility demand per year'
        aliases = ['p_dem_co']
        dependencies = [
            finance.ElectricityDemandMultiplier,
            SocialInfrastructureDemandCurve,
            CommercialFacilityUnitDemandPerCommercialFacilityPerYear,
            demographics.ProjectedPopulationCount,
            ProjectedCommercialFacilityCount,
        ]
        units = 'kilowatt-hours per year'
    
        def compute(self):
            return self.get(finance.ElectricityDemandMultiplier) * self.get(SocialInfrastructureDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(CommercialFacilityUnitDemandPerCommercialFacilityPerYear) * self.get(ProjectedCommercialFacilityCount)



.. _mvmax4-demand-projectededucationfacilitycount:

Projected education facility count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > education facility count curve <mvmax4-demand-educationfacilitycountcurve>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

Derivatives

- :ref:`system (grid) > social infrastructure count <mvmax4-costgrid-gridsocialinfrastructurecount>`

- :ref:`demand (social infrastructure) > projected education facility demand per year <mvmax4-demand-projectededucationfacilitydemandperyear>`


::

    class ProjectedEducationFacilityCount(V):
    
        section = 'demand (social infrastructure)'
        option = 'projected education facility count'
        aliases = ['p_ed']
        dependencies = [
            EducationFacilityCountCurve,
            demographics.ProjectedPopulationCount,
        ]
        units = 'education facility count'
    
        def compute(self):
            return self.get(EducationFacilityCountCurve).interpolate(self.get(demographics.ProjectedPopulationCount))



.. _mvmax4-demand-projectededucationfacilitydemandperyear:

Projected education facility demand per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`finance > electricity demand multiplier <mvmax4-finance-electricitydemandmultiplier>`

- :ref:`demand (social infrastructure) > demand curve <mvmax4-demand-socialinfrastructuredemandcurve>`

- :ref:`demand (social infrastructure) > education facility unit demand per education facility per year <mvmax4-demand-educationfacilityunitdemandpereducationfacilityperyear>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

- :ref:`demand (social infrastructure) > projected education facility count <mvmax4-demand-projectededucationfacilitycount>`

Derivatives

- :ref:`system (off-grid) > photovoltaic panel desired capacity <mvmax4-costoffgrid-photovoltaicpaneldesiredsystemcapacity>`

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`


::

    class ProjectedEducationFacilityDemandPerYear(V):
    
        section = 'demand (social infrastructure)'
        option = 'projected education facility demand per year'
        aliases = ['p_dem_ed']
        dependencies = [
            finance.ElectricityDemandMultiplier,
            SocialInfrastructureDemandCurve,
            EducationFacilityUnitDemandPerEducationFacilityPerYear,
            demographics.ProjectedPopulationCount,
            ProjectedEducationFacilityCount,
        ]
        units = 'kilowatt-hours per year'
    
        def compute(self):
            return self.get(finance.ElectricityDemandMultiplier) * self.get(SocialInfrastructureDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(EducationFacilityUnitDemandPerEducationFacilityPerYear) * self.get(ProjectedEducationFacilityCount)



.. _mvmax4-demand-projectedhealthfacilitycount:

Projected health facility count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > health facility count curve <mvmax4-demand-healthfacilitycountcurve>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

Derivatives

- :ref:`system (grid) > social infrastructure count <mvmax4-costgrid-gridsocialinfrastructurecount>`

- :ref:`demand (social infrastructure) > projected health facility demand per year <mvmax4-demand-projectedhealthfacilitydemandperyear>`


::

    class ProjectedHealthFacilityCount(V):
    
        section = 'demand (social infrastructure)'
        option = 'projected health facility count'
        aliases = ['p_he']
        dependencies = [
            HealthFacilityCountCurve,
            demographics.ProjectedPopulationCount,
        ]
        units = 'health facility count'
    
        def compute(self):
            return self.get(HealthFacilityCountCurve).interpolate(self.get(demographics.ProjectedPopulationCount))



.. _mvmax4-demand-projectedhealthfacilitydemandperyear:

Projected health facility demand per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`finance > electricity demand multiplier <mvmax4-finance-electricitydemandmultiplier>`

- :ref:`demand (social infrastructure) > demand curve <mvmax4-demand-socialinfrastructuredemandcurve>`

- :ref:`demand (social infrastructure) > health facility unit demand per health facility per year <mvmax4-demand-healthfacilityunitdemandperhealthfacilityperyear>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

- :ref:`demand (social infrastructure) > projected health facility count <mvmax4-demand-projectedhealthfacilitycount>`

Derivatives

- :ref:`system (off-grid) > photovoltaic panel desired capacity <mvmax4-costoffgrid-photovoltaicpaneldesiredsystemcapacity>`

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`


::

    class ProjectedHealthFacilityDemandPerYear(V):
    
        section = 'demand (social infrastructure)'
        option = 'projected health facility demand per year'
        aliases = ['p_dem_he']
        dependencies = [
            finance.ElectricityDemandMultiplier,
            SocialInfrastructureDemandCurve,
            HealthFacilityUnitDemandPerHealthFacilityPerYear,
            demographics.ProjectedPopulationCount,
            ProjectedHealthFacilityCount,
        ]
        units = 'kilowatt-hours per year'
    
        def compute(self):
            return self.get(finance.ElectricityDemandMultiplier) * self.get(SocialInfrastructureDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(HealthFacilityUnitDemandPerHealthFacilityPerYear) * self.get(ProjectedHealthFacilityCount)



.. _mvmax4-demand-projectedpubliclightingfacilitycount:

Projected public lighting facility count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > public lighting facility count curve <mvmax4-demand-publiclightingfacilitycountcurve>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

Derivatives

- :ref:`system (grid) > social infrastructure count <mvmax4-costgrid-gridsocialinfrastructurecount>`

- :ref:`demand (social infrastructure) > projected public lighting facility demand per year <mvmax4-demand-projectedpubliclightingfacilitydemandperyear>`


::

    class ProjectedPublicLightingFacilityCount(V):
    
        section = 'demand (social infrastructure)'
        option = 'projected public lighting facility count'
        aliases = ['p_li']
        dependencies = [
            PublicLightingFacilityCountCurve,
            demographics.ProjectedPopulationCount,
        ]
        units = 'public lighting facility count'
    
        def compute(self):
            return self.get(PublicLightingFacilityCountCurve).interpolate(self.get(demographics.ProjectedPopulationCount))



.. _mvmax4-demand-projectedpubliclightingfacilitydemandperyear:

Projected public lighting facility demand per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`finance > electricity demand multiplier <mvmax4-finance-electricitydemandmultiplier>`

- :ref:`demand (social infrastructure) > demand curve <mvmax4-demand-socialinfrastructuredemandcurve>`

- :ref:`demand (social infrastructure) > public lighting facility unit demand per public lighting facility per year <mvmax4-demand-publiclightingfacilityunitdemandperpubliclightingfacilityperyear>`

- :ref:`demographics > projected population count <mvmax4-demographics-projectedpopulationcount>`

- :ref:`demand (social infrastructure) > projected public lighting facility count <mvmax4-demand-projectedpubliclightingfacilitycount>`

Derivatives

- :ref:`system (off-grid) > photovoltaic panel desired capacity <mvmax4-costoffgrid-photovoltaicpaneldesiredsystemcapacity>`

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`


::

    class ProjectedPublicLightingFacilityDemandPerYear(V):
    
        section = 'demand (social infrastructure)'
        option = 'projected public lighting facility demand per year'
        aliases = ['p_dem_li']
        dependencies = [
            finance.ElectricityDemandMultiplier,
            SocialInfrastructureDemandCurve,
            PublicLightingFacilityUnitDemandPerPublicLightingFacilityPerYear,
            demographics.ProjectedPopulationCount,
            ProjectedPublicLightingFacilityCount,
        ]
        units = 'kilowatt-hours per year'
    
        def compute(self):
            return self.get(finance.ElectricityDemandMultiplier) * self.get(SocialInfrastructureDemandCurve).interpolate(self.get(demographics.ProjectedPopulationCount)) * self.get(PublicLightingFacilityUnitDemandPerPublicLightingFacilityPerYear) * self.get(ProjectedPublicLightingFacilityCount)



.. _mvmax4-demand-publiclightingfacilitycountcurve:

Public lighting facility count curve
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > public lighting facility count curve type <mvmax4-demand-publiclightingfacilitycountcurvetype>`

- :ref:`demand (social infrastructure) > public lighting facility count curve points (population and facility count) <mvmax4-demand-publiclightingfacilitycountcurvepoints>`

Derivatives

- :ref:`demand (social infrastructure) > projected public lighting facility count <mvmax4-demand-projectedpubliclightingfacilitycount>`


::

    class PublicLightingFacilityCountCurve(V):
    
        section = 'demand (social infrastructure)'
        option = 'public lighting facility count curve'
        aliases = ['li_cc']
        c = dict(parse=curve.parse, format=curve.format)
        dependencies = [
            PublicLightingFacilityCountCurveType,
            PublicLightingFacilityCountCurvePoints,
        ]
    
        def compute(self):
            curveType = self.get(PublicLightingFacilityCountCurveType)
            curvePoints = self.get(PublicLightingFacilityCountCurvePoints)
            return curve.fit(curveType, curvePoints)



.. _mvmax4-demand-publiclightingfacilitycountcurvepoints:

Public lighting facility count curve points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > public lighting facility count curve <mvmax4-demand-publiclightingfacilitycountcurve>`


::

    class PublicLightingFacilityCountCurvePoints(V):
    
        section = 'demand (social infrastructure)'
        option = 'public lighting facility count curve points (population and facility count)'
        aliases = ['li_cc_pts']
        c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
        default = '50 0.1; 500 1; 5000 7; 10000 25'
        units = 'population and facility count list'



.. _mvmax4-demand-publiclightingfacilitycountcurvetype:

Public lighting facility count curve type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > public lighting facility count curve <mvmax4-demand-publiclightingfacilitycountcurve>`


::

    class PublicLightingFacilityCountCurveType(V):
    
        section = 'demand (social infrastructure)'
        option = 'public lighting facility count curve type'
        aliases = ['li_cc_t']
        c = dict(parse=str, input=curve.inputCurveType)
        default = 'ZeroLogisticLinear'



.. _mvmax4-demand-publiclightingfacilityunitdemandperpubliclightingfacilityperyear:

Public lighting facility unit demand per public lighting facility per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > projected public lighting facility demand per year <mvmax4-demand-projectedpubliclightingfacilitydemandperyear>`


::

    class PublicLightingFacilityUnitDemandPerPublicLightingFacilityPerYear(V):
    
        section = 'demand (social infrastructure)'
        option = 'public lighting facility unit demand per public lighting facility per year'
        aliases = ['li_dc_unit']
        default = 0 # 102
        units = 'kilowatt-hours per year'



.. _mvmax4-demand-socialinfrastructuredemandcurve:

Social infrastructure demand curve
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > demand curve type <mvmax4-demand-socialinfrastructuredemandcurvetype>`

- :ref:`demand (social infrastructure) > demand curve points (population and multiplier) <mvmax4-demand-socialinfrastructuredemandcurvepoints>`

Derivatives

- :ref:`demand (social infrastructure) > projected commercial facility demand per year <mvmax4-demand-projectedcommercialfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected education facility demand per year <mvmax4-demand-projectededucationfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected health facility demand per year <mvmax4-demand-projectedhealthfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected public lighting facility demand per year <mvmax4-demand-projectedpubliclightingfacilitydemandperyear>`


::

    class SocialInfrastructureDemandCurve(V):
    
        section = 'demand (social infrastructure)'
        option = 'demand curve'
        aliases = ['so_dc']
        c = dict(parse=curve.parse, format=curve.format)
        dependencies = [
            SocialInfrastructureDemandCurveType,
            SocialInfrastructureDemandCurvePoints,
        ]
    
        def compute(self):
            curveType = self.get(SocialInfrastructureDemandCurveType)
            curvePoints = self.get(SocialInfrastructureDemandCurvePoints)
            return curve.fit(curveType, curvePoints)



.. _mvmax4-demand-socialinfrastructuredemandcurvepoints:

Social infrastructure demand curve points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > demand curve <mvmax4-demand-socialinfrastructuredemandcurve>`


::

    class SocialInfrastructureDemandCurvePoints(V):
    
        section = 'demand (social infrastructure)'
        option = 'demand curve points (population and multiplier)'
        aliases = ['so_dc_pts']
        c = dict(parse=store.unstringifyCoordinatesList, format=store.flattenCoordinatesList, validate='validateCoordinatesList')
        default = '500 1; 1000 1.5; 5000 2.25; 10000 3.375' 
        units = 'population and multiplier list'



.. _mvmax4-demand-socialinfrastructuredemandcurvetype:

Social infrastructure demand curve type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`demand (social infrastructure) > demand curve <mvmax4-demand-socialinfrastructuredemandcurve>`


::

    class SocialInfrastructureDemandCurveType(V):
    
        section = 'demand (social infrastructure)'
        option = 'demand curve type'
        aliases = ['so_dc_t']
        c = dict(parse=str, input=curve.inputCurveType)
        default = 'ZeroLogisticLinear'



Distribution
------------

.. _mvmax4-costdistribution-lowvoltagelinecostpermeter:

Low voltage line cost per meter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`distribution > low voltage line initial cost <mvmax4-costdistribution-lowvoltagelineinitialcost>`

- :ref:`distribution > low voltage line operations and maintenance cost per year <mvmax4-costdistribution-lowvoltagelineoperationsandmaintenancecostperyear>`


::

    class LowVoltageLineCostPerMeter(V):
    
        section = 'distribution'
        option = 'low voltage line cost per meter'
        aliases = ['di_ll_cm']
        default = 10
        units = 'dollars per meter'



.. _mvmax4-costdistribution-lowvoltagelineequipmentcostperconnection:

Low voltage line equipment cost per connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > low voltage line equipment cost <mvmax4-costgrid-lowvoltagelineequipmentcost>`

- :ref:`system (mini-grid) > low voltage line equipment cost <mvmax4-costminigrid-lowvoltagelineequipmentcost>`


::

    class LowVoltageLineEquipmentCostPerConnection(V):
    
        section = 'distribution'
        option = 'low voltage line equipment cost per connection'
        aliases = ['di_le_cc']
        default = 200
        units = 'dollars per connection'



.. _mvmax4-costdistribution-lowvoltagelineequipmentoperationsandmaintenancecostperyearasfractionofequipmentcost:

Low voltage line equipment operations and maintenance cost per year as fraction of equipment cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > low voltage line equipment operations and maintenance cost per year <mvmax4-costminigrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear>`

- :ref:`system (grid) > low voltage line equipment operations and maintenance cost per year <mvmax4-costgrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear>`


::

    class LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost(V):
    
        section = 'distribution'
        option = 'low voltage line equipment operations and maintenance cost as fraction of equipment cost'
        aliases = ['di_le_omf']
        default = 0.01



.. _mvmax4-costdistribution-lowvoltagelineinitialcost:

Low voltage line initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`distribution > low voltage line length <mvmax4-costdistribution-lowvoltagelinelength>`

- :ref:`distribution > low voltage line cost per meter <mvmax4-costdistribution-lowvoltagelinecostpermeter>`

Derivatives

- :ref:`system (grid) > internal system initial cost <mvmax4-costgrid-gridinternalsysteminitialcost>`

- :ref:`distribution > low voltage line replacement cost per year <mvmax4-costdistribution-lowvoltagelinereplacementcostperyear>`

- :ref:`system (mini-grid) > system initial cost <mvmax4-costminigrid-minigridsysteminitialcost>`


::

    class LowVoltageLineInitialCost(V):
    
        section = 'distribution'
        option = 'low voltage line initial cost'
        aliases = ['di_ll_ini']
        dependencies = [
            LowVoltageLineLength,
            LowVoltageLineCostPerMeter,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(LowVoltageLineCostPerMeter) * self.get(LowVoltageLineLength)



.. _mvmax4-costdistribution-lowvoltagelinelength:

Low voltage line length
^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demographics > mean interhousehold distance <mvmax4-demographics-meaninterhouseholddistance>`

- :ref:`demand (household) > target household count <mvmax4-demand-targethouseholdcount>`

Derivatives

- :ref:`distribution > low voltage line initial cost <mvmax4-costdistribution-lowvoltagelineinitialcost>`

- :ref:`distribution > low voltage line operations and maintenance cost per year <mvmax4-costdistribution-lowvoltagelineoperationsandmaintenancecostperyear>`


::

    class LowVoltageLineLength(V):
    
        section = 'distribution'
        option = 'low voltage line length'
        aliases = ['di_ll_len']
        dependencies = [
            demographics.MeanInterhouseholdDistance,
            demand.TargetHouseholdCount,
        ]
        units = 'meters'
    
        def compute(self):
            # Load
            meanInterhouseholdDistance = self.get(demographics.MeanInterhouseholdDistance)
            targetHouseholdCount = self.get(demand.TargetHouseholdCount)
            # Return
            return meanInterhouseholdDistance * (targetHouseholdCount - 1) if targetHouseholdCount > 1 else 0



.. _mvmax4-costdistribution-lowvoltagelinelifetime:

Low voltage line lifetime
^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`distribution > low voltage line replacement cost per year <mvmax4-costdistribution-lowvoltagelinereplacementcostperyear>`


::

    class LowVoltageLineLifetime(V):
    
        section = 'distribution'
        option = 'low voltage line lifetime'
        aliases = ['di_ll_life']
        c = dict(check=store.assertPositive)
        default = 10
        units = 'years'



.. _mvmax4-costdistribution-lowvoltagelineoperationsandmaintenancecostperyear:

Low voltage line operations and maintenance cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`distribution > low voltage line operations and maintenance cost per year as fraction of line cost <mvmax4-costdistribution-lowvoltagelineoperationsandmaintenancecostperyearasfractionoflinecost>`

- :ref:`distribution > low voltage line cost per meter <mvmax4-costdistribution-lowvoltagelinecostpermeter>`

- :ref:`distribution > low voltage line length <mvmax4-costdistribution-lowvoltagelinelength>`

Derivatives

- :ref:`distribution > low voltage line recurring cost per year <mvmax4-costdistribution-lowvoltagelinerecurringcostperyear>`


::

    class LowVoltageLineOperationsAndMaintenanceCostPerYear(V):
    
        section = 'distribution'
        option = 'low voltage line operations and maintenance cost per year'
        aliases = ['di_ll_om']
        dependencies = [
            LowVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost,
            LowVoltageLineCostPerMeter,
            LowVoltageLineLength,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(LowVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost) * self.get(LowVoltageLineCostPerMeter) * self.get(LowVoltageLineLength)



.. _mvmax4-costdistribution-lowvoltagelineoperationsandmaintenancecostperyearasfractionoflinecost:

Low voltage line operations and maintenance cost per year as fraction of line cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`distribution > low voltage line operations and maintenance cost per year <mvmax4-costdistribution-lowvoltagelineoperationsandmaintenancecostperyear>`


::

    class LowVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost(V):
    
        section = 'distribution'
        option = 'low voltage line operations and maintenance cost per year as fraction of line cost'
        aliases = ['di_ll_omf']
        default = 0.01



.. _mvmax4-costdistribution-lowvoltagelinerecurringcostperyear:

Low voltage line recurring cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`distribution > low voltage line operations and maintenance cost per year <mvmax4-costdistribution-lowvoltagelineoperationsandmaintenancecostperyear>`

- :ref:`distribution > low voltage line replacement cost per year <mvmax4-costdistribution-lowvoltagelinereplacementcostperyear>`

Derivatives

- :ref:`system (grid) > internal system recurring cost per year <mvmax4-costgrid-gridinternalsystemrecurringcostperyear>`

- :ref:`system (mini-grid) > system recurring cost per year <mvmax4-costminigrid-minigridsystemrecurringcostperyear>`


::

    class LowVoltageLineRecurringCostPerYear(V):
    
        section = 'distribution'
        option = 'low voltage line recurring cost per year'
        aliases = ['di_ll_rec']
        dependencies = [
            LowVoltageLineOperationsAndMaintenanceCostPerYear,
            LowVoltageLineReplacementCostPerYear,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return sum([
                self.get(LowVoltageLineOperationsAndMaintenanceCostPerYear),
                self.get(LowVoltageLineReplacementCostPerYear),
            ])



.. _mvmax4-costdistribution-lowvoltagelinereplacementcostperyear:

Low voltage line replacement cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`distribution > low voltage line initial cost <mvmax4-costdistribution-lowvoltagelineinitialcost>`

- :ref:`distribution > low voltage line lifetime <mvmax4-costdistribution-lowvoltagelinelifetime>`

Derivatives

- :ref:`distribution > low voltage line recurring cost per year <mvmax4-costdistribution-lowvoltagelinerecurringcostperyear>`


::

    class LowVoltageLineReplacementCostPerYear(V):
    
        section = 'distribution'
        option = 'low voltage line replacement cost per year'
        aliases = ['di_ll_rep']
        dependencies = [
            LowVoltageLineInitialCost,
            LowVoltageLineLifetime,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(LowVoltageLineInitialCost) / float(self.get(LowVoltageLineLifetime))



System (off-grid)
-----------------

.. _mvmax4-costoffgrid-dieselcomponentinitialcost:

Diesel component initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > diesel generator cost <mvmax4-costoffgrid-dieselgeneratorcost>`

- :ref:`system (off-grid) > diesel generator installation cost <mvmax4-costoffgrid-dieselgeneratorinstallationcost>`

Derivatives

- :ref:`system (off-grid) > system initial cost <mvmax4-costoffgrid-offgridsysteminitialcost>`


::

    class DieselComponentInitialCost(costMiniGrid.MiniGridSystemInitialCost):
    
        section = 'system (off-grid)'
        option = 'diesel component initial cost'
        aliases = ['og_d_ini']
        dependencies = [
            DieselGeneratorCost,
            DieselGeneratorInstallationCost,
        ]
    
        def compute(self):
            return sum([
                self.get(DieselGeneratorCost),
                self.get(DieselGeneratorInstallationCost),
            ])



.. _mvmax4-costoffgrid-dieselcomponentrecurringcostperyear:

Diesel component recurring cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > diesel generator operations and maintenance cost per year <mvmax4-costoffgrid-dieselgeneratoroperationsandmaintenancecostperyear>`

- :ref:`system (off-grid) > diesel generator replacement cost per year <mvmax4-costoffgrid-dieselgeneratorreplacementcostperyear>`

- :ref:`system (off-grid) > diesel fuel cost per year <mvmax4-costoffgrid-dieselfuelcostperyear>`

Derivatives

- :ref:`system (off-grid) > system recurring cost per year <mvmax4-costoffgrid-offgridsystemrecurringcostperyear>`


::

    class DieselComponentRecurringCostPerYear(costMiniGrid.MiniGridSystemRecurringCostPerYear):
    
        section = 'system (off-grid)'
        option = 'diesel component recurring cost per year'
        aliases = ['og_d_rec']
        dependencies = [
            DieselGeneratorOperationsAndMaintenanceCostPerYear,
            DieselGeneratorReplacementCostPerYear,
            DieselFuelCostPerYear,
        ]
    
        def compute(self):
            return sum([
                self.get(DieselGeneratorOperationsAndMaintenanceCostPerYear),
                self.get(DieselGeneratorReplacementCostPerYear),
                self.get(DieselFuelCostPerYear),
            ])



.. _mvmax4-costoffgrid-dieselfuelcostperyear:

Diesel fuel cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel fuel cost per liter <mvmax4-costminigrid-dieselfuelcostperliter>`

- :ref:`system (mini-grid) > diesel fuel liters consumed per kilowatt-hour <mvmax4-costminigrid-dieselfuellitersconsumedperkilowatthour>`

- :ref:`system (off-grid) > diesel generator actual system capacity <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacity>`

- :ref:`system (off-grid) > diesel generator hours of operation per year (effective) <mvmax4-costoffgrid-dieselgeneratoreffectivehoursofoperationperyear>`

Derivatives

- :ref:`system (off-grid) > diesel component recurring cost per year <mvmax4-costoffgrid-dieselcomponentrecurringcostperyear>`


::

    class DieselFuelCostPerYear(costMiniGrid.DieselFuelCostPerYear):
    
        section = 'system (off-grid)'
        aliases = ['og_fl']
        dependencies = [
            costMiniGrid.DieselFuelCostPerLiter,
            costMiniGrid.DieselFuelLitersConsumedPerKilowattHour,
            DieselGeneratorActualSystemCapacity,
            DieselGeneratorEffectiveHoursOfOperationPerYear,
        ]
    
        def compute(self):
            return self.get(costMiniGrid.DieselFuelCostPerLiter) * self.get(costMiniGrid.DieselFuelLitersConsumedPerKilowattHour) * self.get(DieselGeneratorActualSystemCapacity) * self.get(DieselGeneratorEffectiveHoursOfOperationPerYear)



.. _mvmax4-costoffgrid-dieselgeneratoractualsystemcapacity:

Diesel generator actual system capacity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > available system capacities (diesel generator) <mvmax4-costoffgrid-dieselgeneratoravailablesystemcapacities>`

- :ref:`system (off-grid) > diesel generator actual system capacity counts <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacitycounts>`

Derivatives

- :ref:`system (off-grid) > diesel fuel cost per year <mvmax4-costoffgrid-dieselfuelcostperyear>`

- :ref:`system (off-grid) > diesel generator cost <mvmax4-costoffgrid-dieselgeneratorcost>`

- :ref:`system (off-grid) > diesel generator hours of operation per year (effective) <mvmax4-costoffgrid-dieselgeneratoreffectivehoursofoperationperyear>`


::

    class DieselGeneratorActualSystemCapacity(costMiniGrid.DieselGeneratorActualSystemCapacity):
    
        section = 'system (off-grid)'
        aliases = ['og_dg_acp']
        dependencies = [
            DieselGeneratorAvailableSystemCapacities,
            DieselGeneratorActualSystemCapacityCounts,
        ]
    
        def compute(self):
            return numpy.dot(
                self.get(DieselGeneratorAvailableSystemCapacities), 
                self.get(DieselGeneratorActualSystemCapacityCounts))



.. _mvmax4-costoffgrid-dieselgeneratoractualsystemcapacitycounts:

Diesel generator actual system capacity counts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > diesel generator desired system capacity <mvmax4-costoffgrid-dieselgeneratordesiredsystemcapacity>`

- :ref:`system (off-grid) > available system capacities (diesel generator) <mvmax4-costoffgrid-dieselgeneratoravailablesystemcapacities>`

Derivatives

- :ref:`system (off-grid) > diesel generator actual system capacity <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacity>`


::

    class DieselGeneratorActualSystemCapacityCounts(costMiniGrid.DieselGeneratorActualSystemCapacityCounts):
    
        section = 'system (off-grid)'
        aliases = ['og_dg_acps']
        dependencies = [
            DieselGeneratorDesiredSystemCapacity,
            DieselGeneratorAvailableSystemCapacities,
        ]
    
        def compute(self):
            return metric.computeSystemCounts(
                self.get(DieselGeneratorDesiredSystemCapacity), 
                self.get(DieselGeneratorAvailableSystemCapacities))



.. _mvmax4-costoffgrid-dieselgeneratoravailablesystemcapacities:

Diesel generator available system capacities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > diesel generator actual system capacity <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacity>`

- :ref:`system (off-grid) > diesel generator actual system capacity counts <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacitycounts>`


::

    class DieselGeneratorAvailableSystemCapacities(costMiniGrid.DieselGeneratorAvailableSystemCapacities):
    
        section = 'system (off-grid)'
        default = '1000 750 500 400 200 150 100 70 32 19 12 10 8 6'
        aliases = ['og_dg_cps']



.. _mvmax4-costoffgrid-dieselgeneratorcost:

Diesel generator cost
^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator cost per diesel system kilowatt <mvmax4-costminigrid-dieselgeneratorcostperdieselsystemkilowatt>`

- :ref:`system (off-grid) > diesel generator actual system capacity <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacity>`

Derivatives

- :ref:`system (off-grid) > diesel component initial cost <mvmax4-costoffgrid-dieselcomponentinitialcost>`

- :ref:`system (off-grid) > diesel generator installation cost <mvmax4-costoffgrid-dieselgeneratorinstallationcost>`

- :ref:`system (off-grid) > diesel generator operations and maintenance cost per year <mvmax4-costoffgrid-dieselgeneratoroperationsandmaintenancecostperyear>`

- :ref:`system (off-grid) > diesel generator replacement cost per year <mvmax4-costoffgrid-dieselgeneratorreplacementcostperyear>`


::

    class DieselGeneratorCost(costMiniGrid.DieselGeneratorCost):
    
        section = 'system (off-grid)'
        aliases = ['og_dg_ini']
        dependencies = [
            costMiniGrid.DieselGeneratorCostPerDieselSystemKilowatt,
            DieselGeneratorActualSystemCapacity,
        ]
    
        def compute(self):
            return self.get(costMiniGrid.DieselGeneratorCostPerDieselSystemKilowatt) * self.get(DieselGeneratorActualSystemCapacity)



.. _mvmax4-costoffgrid-dieselgeneratordesiredsystemcapacity:

Diesel generator desired system capacity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (peak) > projected peak commercial facility demand <mvmax4-demand-projectedpeakcommercialfacilitydemand>`

- :ref:`demand (peak) > projected peak productive demand <mvmax4-demand-projectedpeakproductivedemand>`

Derivatives

- :ref:`system (off-grid) > diesel generator actual system capacity counts <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacitycounts>`


::

    class DieselGeneratorDesiredSystemCapacity(costMiniGrid.DieselGeneratorDesiredSystemCapacity):
    
        section = 'system (off-grid)'
        aliases = ['og_dg_dcp']
        dependencies = [
            demand.ProjectedPeakCommercialFacilityDemand,
            demand.ProjectedPeakProductiveDemand,
        ]
    
        def compute(self):
            return sum([
                self.get(demand.ProjectedPeakCommercialFacilityDemand),
                self.get(demand.ProjectedPeakProductiveDemand),
            ])



.. _mvmax4-costoffgrid-dieselgeneratoreffectivehoursofoperationperyear:

Diesel generator effective hours of operation per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > projected commercial facility demand per year <mvmax4-demand-projectedcommercialfacilitydemandperyear>`

- :ref:`demand (productive) > projected productive demand <mvmax4-demand-projectedproductivedemandperyear>`

- :ref:`system (off-grid) > diesel generator hours of operation per year (minimum) <mvmax4-costoffgrid-dieselgeneratorminimumhoursofoperationperyear>`

- :ref:`system (off-grid) > diesel generator actual system capacity <mvmax4-costoffgrid-dieselgeneratoractualsystemcapacity>`

Derivatives

- :ref:`system (off-grid) > diesel fuel cost per year <mvmax4-costoffgrid-dieselfuelcostperyear>`


::

    class DieselGeneratorEffectiveHoursOfOperationPerYear(V):
    
        section = 'system (off-grid)'
        option = 'diesel generator hours of operation per year (effective)'
        aliases = ['og_dg_efhr']
        dependencies = [
            demand.ProjectedCommercialFacilityDemandPerYear,
            demand.ProjectedProductiveDemandPerYear,
            DieselGeneratorMinimumHoursOfOperationPerYear,
            DieselGeneratorActualSystemCapacity,
        ]
        units = 'hours per year'
    
        def compute(self):
            # Initialize
            dieselGeneratorActualSystemCapacity = self.get(DieselGeneratorActualSystemCapacity)
            # If the capacity of the diesel generator is zero,
            if dieselGeneratorActualSystemCapacity == 0:
                # Return zero hours of operation
                return 0
            # Compute effectiveDemandPerYear and assume an off-grid diesel generator does NOT have distribution loss
            effectiveDemandPerYear = self.get(demand.ProjectedCommercialFacilityDemandPerYear) + self.get(demand.ProjectedProductiveDemandPerYear)
            # Return
            return max(self.get(DieselGeneratorMinimumHoursOfOperationPerYear), effectiveDemandPerYear / float(dieselGeneratorActualSystemCapacity))



.. _mvmax4-costoffgrid-dieselgeneratorinstallationcost:

Diesel generator installation cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator installation cost as fraction of generator cost <mvmax4-costminigrid-dieselgeneratorinstallationcostasfractionofgeneratorcost>`

- :ref:`system (off-grid) > diesel generator cost <mvmax4-costoffgrid-dieselgeneratorcost>`

Derivatives

- :ref:`system (off-grid) > diesel component initial cost <mvmax4-costoffgrid-dieselcomponentinitialcost>`


::

    class DieselGeneratorInstallationCost(costMiniGrid.DieselGeneratorInstallationCost):
    
        section = 'system (off-grid)'
        aliases = ['og_dg_i']
        dependencies = [
            costMiniGrid.DieselGeneratorInstallationCostAsFractionOfGeneratorCost,
            DieselGeneratorCost,
        ]
    
        def compute(self):
            return self.get(costMiniGrid.DieselGeneratorInstallationCostAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)



.. _mvmax4-costoffgrid-dieselgeneratorminimumhoursofoperationperyear:

Diesel generator minimum hours of operation per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > diesel generator hours of operation per year (effective) <mvmax4-costoffgrid-dieselgeneratoreffectivehoursofoperationperyear>`


::

    class DieselGeneratorMinimumHoursOfOperationPerYear(V):
    
        section = 'system (off-grid)'
        option = 'diesel generator hours of operation per year (minimum)'
        aliases = ['og_dg_mnhr']
        default = 1460
        units = 'hours per year'



.. _mvmax4-costoffgrid-dieselgeneratoroperationsandmaintenancecostperyear:

Diesel generator operations and maintenance cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator operations and maintenance cost per year as fraction of generator cost <mvmax4-costminigrid-dieselgeneratoroperationsandmaintenancecostperyearasfractionofgeneratorcost>`

- :ref:`system (off-grid) > diesel generator cost <mvmax4-costoffgrid-dieselgeneratorcost>`

Derivatives

- :ref:`system (off-grid) > diesel component recurring cost per year <mvmax4-costoffgrid-dieselcomponentrecurringcostperyear>`


::

    class DieselGeneratorOperationsAndMaintenanceCostPerYear(costMiniGrid.DieselGeneratorOperationsAndMaintenanceCostPerYear):
    
        section = 'system (off-grid)'
        aliases = ['og_dg_om']
        dependencies = [
            costMiniGrid.DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost,
            DieselGeneratorCost,
        ]
    
        def compute(self):
            return self.get(costMiniGrid.DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)



.. _mvmax4-costoffgrid-dieselgeneratorreplacementcostperyear:

Diesel generator replacement cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > diesel generator cost <mvmax4-costoffgrid-dieselgeneratorcost>`

- :ref:`system (mini-grid) > diesel generator lifetime <mvmax4-costminigrid-dieselgeneratorlifetime>`

Derivatives

- :ref:`system (off-grid) > diesel component recurring cost per year <mvmax4-costoffgrid-dieselcomponentrecurringcostperyear>`


::

    class DieselGeneratorReplacementCostPerYear(costMiniGrid.DieselGeneratorReplacementCostPerYear):
    
        section = 'system (off-grid)'
        aliases = ['og_dg_rep']
        dependencies = [
            DieselGeneratorCost,
            costMiniGrid.DieselGeneratorLifetime,
        ]
    
        def compute(self):
            return self.get(DieselGeneratorCost) / float(self.get(costMiniGrid.DieselGeneratorLifetime))



.. _mvmax4-costoffgrid-offgridsysteminitialcost:

Off grid system initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic component initial cost <mvmax4-costoffgrid-photovoltaiccomponentinitialcost>`

- :ref:`system (off-grid) > diesel component initial cost <mvmax4-costoffgrid-dieselcomponentinitialcost>`

Derivatives

- :ref:`system (off-grid) > system nodal discounted cost <mvmax4-costoffgrid-offgridsystemnodaldiscountedcost>`


::

    class OffGridSystemInitialCost(V):
    
        section = 'system (off-grid)'
        option = 'system initial cost'
        aliases = ['og_ini']
        dependencies = [
            PhotovoltaicComponentInitialCost,
            DieselComponentInitialCost,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(PhotovoltaicComponentInitialCost) + self.get(DieselComponentInitialCost)



.. _mvmax4-costoffgrid-offgridsystemnodaldiscountedcost:

Off grid system nodal discounted cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`system (off-grid) > system initial cost <mvmax4-costoffgrid-offgridsysteminitialcost>`

- :ref:`system (off-grid) > system recurring cost per year <mvmax4-costoffgrid-offgridsystemrecurringcostperyear>`

- :ref:`finance > discounted cash flow factor <mvmax4-finance-discountedcashflowfactor>`

Derivatives

- :ref:`metric > maximum length of medium voltage line extension <mvmax4-metric>`

- :ref:`system (off-grid) > system nodal levelized cost <mvmax4-costoffgrid-offgridsystemnodallevelizedcost>`

- :ref:`metric > system <mvmax4-system>`


::

    class OffGridSystemNodalDiscountedCost(V):
    
        section = 'system (off-grid)'
        option = 'system nodal discounted cost'
        aliases = ['og_nod_d']
        dependencies = [
            demand.ProjectedNodalDemandPerYear,
            OffGridSystemInitialCost,
            OffGridSystemRecurringCostPerYear,
            finance.DiscountedCashFlowFactor,
        ]
        units = 'dollars'
    
        def compute(self):
            if self.get(demand.ProjectedNodalDemandPerYear) == 0:
                return 0
            return self.get(OffGridSystemInitialCost) + self.get(OffGridSystemRecurringCostPerYear) * self.get(finance.DiscountedCashFlowFactor)



.. _mvmax4-costoffgrid-offgridsystemnodallevelizedcost:

Off grid system nodal levelized cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand > projected nodal discounted demand <mvmax4-demand-projectednodaldiscounteddemand>`

- :ref:`system (off-grid) > system nodal discounted cost <mvmax4-costoffgrid-offgridsystemnodaldiscountedcost>`

Derivatives

- :ref:`metric > maximum length of medium voltage line extension <mvmax4-metric>`


::

    class OffGridSystemNodalLevelizedCost(V):
    
        section = 'system (off-grid)'
        option = 'system nodal levelized cost'
        aliases = ['og_nod_lev']
        dependencies = [
            demand.ProjectedNodalDiscountedDemand,
            OffGridSystemNodalDiscountedCost,
        ]
        units = 'dollars per kilowatt-hour'
    
        def compute(self):
            if self.get(demand.ProjectedNodalDiscountedDemand) == 0:
                return 0
            return self.get(OffGridSystemNodalDiscountedCost) / float(self.get(demand.ProjectedNodalDiscountedDemand))



.. _mvmax4-costoffgrid-offgridsystemrecurringcostperyear:

Off grid system recurring cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic component recurring cost per year <mvmax4-costoffgrid-photovoltaiccomponentrecurringcostperyear>`

- :ref:`system (off-grid) > diesel component recurring cost per year <mvmax4-costoffgrid-dieselcomponentrecurringcostperyear>`

Derivatives

- :ref:`system (off-grid) > system nodal discounted cost <mvmax4-costoffgrid-offgridsystemnodaldiscountedcost>`


::

    class OffGridSystemRecurringCostPerYear(V):
    
        section = 'system (off-grid)'
        option = 'system recurring cost per year'
        aliases = ['og_rec']
        dependencies = [
            PhotovoltaicComponentRecurringCostPerYear,
            DieselComponentRecurringCostPerYear,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(PhotovoltaicComponentRecurringCostPerYear) + self.get(DieselComponentRecurringCostPerYear)



.. _mvmax4-offgridsystemtotal:

Off grid system total
^^^^^^^^^^^^^^^^^^^^^


::

    class OffGridSystemTotal(V):
    
        section = 'system (off-grid)'
        option = 'system total'
        aliases = ['og_ct']
        default = 0
        units = 'count'
    
        def aggregate(self, childVS):
            # If the system is off-grid,
            if childVS.get(System)[0] == 'o':
                # Update
                self.value += 1



.. _mvmax4-offgridsystemtotaldiscountedcost:

Off grid system total discounted cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > system total levelized cost <mvmax4-offgridsystemtotallevelizedcost>`


::

    class OffGridSystemTotalDiscountedCost(V):
    
        section = 'system (off-grid)'
        option = 'system total discounted cost'
        aliases = ['og_tot_d']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # If the system is off-grid,
            if childVS.get(System)[0] == 'o':
                # Update
                self.value += childVS.get(costOffGrid.OffGridSystemNodalDiscountedCost)



.. _mvmax4-offgridsystemtotaldiscounteddemand:

Off grid system total discounted demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > system total levelized cost <mvmax4-offgridsystemtotallevelizedcost>`


::

    class OffGridSystemTotalDiscountedDemand(V):
    
        section = 'system (off-grid)'
        option = 'system total discounted demand'
        aliases = ['og_dem_d']
        default = 0
        units = 'kilowatt-hours'
    
        def aggregate(self, childVS):
            # If the system is off-grid,
            if childVS.get(System)[0] == 'o':
                # Update
                self.value += childVS.get(demand.ProjectedNodalDiscountedDemand)



.. _mvmax4-offgridsystemtotaldiscounteddieselcost:

Off grid system total discounted diesel cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


::

    class OffGridSystemTotalDiscountedDieselCost(V):
    
        section = 'system (off-grid)'
        option = 'system total discounted diesel cost'
        aliases = ['og_tot_ddc']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # If the system is off-grid,
            if childVS.get(System)[0] == 'o':
                # add up nodal diesel costs
                self.value += childVS.get(costOffGrid.OffGridSystemNodalDiscountedDieselCost) 



.. _mvmax4-offgridsystemtotaldiscounteddieselfuelcost:

Off grid system total discounted diesel fuel cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


::

    class OffGridSystemTotalDiscountedDieselFuelCost(V):
    
        section = 'system (off-grid)'
        option = 'system total discounted diesel fuel cost'
        aliases = ['og_tot_ddfc']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # If the system is off-grid,
            if childVS.get(System)[0] == 'o':
                # add up nodal diesel costs
                self.value += childVS.get(costOffGrid.OffGridSystemNodalDiscountedDieselFuelCost) 



.. _mvmax4-offgridsystemtotaldiscountedrecurringcost:

Off grid system total discounted recurring cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


::

    class OffGridSystemTotalDiscountedRecurringCost(V):
    
        section = 'system (off-grid)'
        option = 'system total discounted recurring cost'
        aliases = ['og_tot_drc']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # If the system is off-grid,
            if childVS.get(System)[0] == 'o':
                # Update
                self.value += ( \
                        childVS.get(costOffGrid.OffGridSystemRecurringCostPerYear) * \
                        childVS.get(finance.DiscountedCashFlowFactor))



.. _mvmax4-offgridsystemtotalinitialcost:

Off grid system total initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


::

    class OffGridSystemTotalInitialCost(V):
    
        section = 'system (off-grid)'
        option = 'system total initial cost'
        aliases = ['og_tot_i']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # If the system is off-grid,
            if childVS.get(System)[0] == 'o':
                # Update
                self.value += childVS.get(costOffGrid.OffGridSystemInitialCost)



.. _mvmax4-offgridsystemtotallevelizedcost:

Off grid system total levelized cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > system total discounted demand <mvmax4-offgridsystemtotaldiscounteddemand>`

- :ref:`system (off-grid) > system total discounted cost <mvmax4-offgridsystemtotaldiscountedcost>`


::

    class OffGridSystemTotalLevelizedCost(V):
    
        section = 'system (off-grid)'
        option = 'system total levelized cost'
        aliases = ['og_tot_lev']
        dependencies = [
            OffGridSystemTotalDiscountedDemand,
            OffGridSystemTotalDiscountedCost,
        ]
        units = 'dollars per kilowatt-hour'
    
        def compute(self):
            if self.get(OffGridSystemTotalDiscountedDemand) == 0:
                return 0
            return self.get(OffGridSystemTotalDiscountedCost) / float(self.get(OffGridSystemTotalDiscountedDemand))



.. _mvmax4-costoffgrid-peaksunhoursperyear:

Peak sun hours per year
^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic panel desired capacity <mvmax4-costoffgrid-photovoltaicpaneldesiredsystemcapacity>`


::

    class PeakSunHoursPerYear(V):
        """
        Peak sun hours is the number of hours per year during which sunlight
        is considered brightest for a given location.
        """
    
        section = 'system (off-grid)'
        option = 'peak sun hours per year'
        aliases = ['pksu_hr']
        c = dict(check=store.assertPositive)
        default = 1320
        units = 'hours per year'



.. _mvmax4-costoffgrid-photovoltaicbalancecost:

Photovoltaic balance cost
^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic balance cost as fraction of panel cost <mvmax4-costoffgrid-photovoltaicbalancecostasfractionofpanelcost>`

- :ref:`system (off-grid) > photovoltaic panel cost <mvmax4-costoffgrid-photovoltaicpanelcost>`

Derivatives

- :ref:`system (off-grid) > photovoltaic balance replacement cost per year <mvmax4-costoffgrid-photovoltaicbalancereplacementcostperyear>`

- :ref:`system (off-grid) > photovoltaic component initial cost <mvmax4-costoffgrid-photovoltaiccomponentinitialcost>`


::

    class PhotovoltaicBalanceCost(V):
        """
        The balance consists of the parts of the photovoltaic system besides 
        the panels and the batteries.
        """
    
        section = 'system (off-grid)'
        option = 'photovoltaic balance cost'
        aliases = ['og_px_ini']
        dependencies = [
            PhotovoltaicBalanceCostAsFractionOfPanelCost,
            PhotovoltaicPanelCost,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(PhotovoltaicBalanceCostAsFractionOfPanelCost) * self.get(PhotovoltaicPanelCost)



.. _mvmax4-costoffgrid-photovoltaicbalancecostasfractionofpanelcost:

Photovoltaic balance cost as fraction of panel cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic balance cost <mvmax4-costoffgrid-photovoltaicbalancecost>`


::

    class PhotovoltaicBalanceCostAsFractionOfPanelCost(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic balance cost as fraction of panel cost'
        aliases = ['og_px_cf']
        default = 0.5



.. _mvmax4-costoffgrid-photovoltaicbalancelifetime:

Photovoltaic balance lifetime
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic balance replacement cost per year <mvmax4-costoffgrid-photovoltaicbalancereplacementcostperyear>`


::

    class PhotovoltaicBalanceLifetime(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic balance lifetime'
        aliases = ['og_px_life']
        c = dict(check=store.assertPositive)
        default = 10
        units = 'years'



.. _mvmax4-costoffgrid-photovoltaicbalancereplacementcostperyear:

Photovoltaic balance replacement cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic balance cost <mvmax4-costoffgrid-photovoltaicbalancecost>`

- :ref:`system (off-grid) > photovoltaic balance lifetime <mvmax4-costoffgrid-photovoltaicbalancelifetime>`

Derivatives

- :ref:`system (off-grid) > photovoltaic component recurring cost per year <mvmax4-costoffgrid-photovoltaiccomponentrecurringcostperyear>`


::

    class PhotovoltaicBalanceReplacementCostPerYear(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic balance replacement cost per year'
        aliases = ['og_px_rep']
        dependencies = [
            PhotovoltaicBalanceCost,
            PhotovoltaicBalanceLifetime,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(PhotovoltaicBalanceCost) / float(self.get(PhotovoltaicBalanceLifetime))



.. _mvmax4-costoffgrid-photovoltaicbatterycost:

Photovoltaic battery cost
^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic battery cost per kilowatt-hour <mvmax4-costoffgrid-photovoltaicbatterycostperkilowatthour>`

- :ref:`system (off-grid) > photovoltaic battery kilowatt-hours per photovoltaic component kilowatt <mvmax4-costoffgrid-photovoltaicbatterykilowatthoursperphotovoltaiccomponentkilowatt>`

- :ref:`system (off-grid) > photovoltaic panel actual capacity <mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacity>`

Derivatives

- :ref:`system (off-grid) > photovoltaic battery replacement cost per year <mvmax4-costoffgrid-photovoltaicbatteryreplacementcostperyear>`

- :ref:`system (off-grid) > photovoltaic component initial cost <mvmax4-costoffgrid-photovoltaiccomponentinitialcost>`


::

    class PhotovoltaicBatteryCost(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic battery cost'
        aliases = ['og_pb_ini']
        dependencies = [
            PhotovoltaicBatteryCostPerKilowattHour,
            PhotovoltaicBatteryKilowattHoursPerPhotovoltaicComponentKilowatt,
            PhotovoltaicPanelActualSystemCapacity,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(PhotovoltaicBatteryCostPerKilowattHour) * self.get(PhotovoltaicBatteryKilowattHoursPerPhotovoltaicComponentKilowatt) * self.get(PhotovoltaicPanelActualSystemCapacity)



.. _mvmax4-costoffgrid-photovoltaicbatterycostperkilowatthour:

Photovoltaic battery cost per kilowatt hour
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic battery cost <mvmax4-costoffgrid-photovoltaicbatterycost>`


::

    class PhotovoltaicBatteryCostPerKilowattHour(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic battery cost per kilowatt-hour'
        aliases = ['og_pb_ckwh']
        default = 400
        units = 'dollars per kilowatt-hour'



.. _mvmax4-costoffgrid-photovoltaicbatterykilowatthoursperphotovoltaiccomponentkilowatt:

Photovoltaic battery kilowatt hours per photovoltaic component kilowatt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic battery cost <mvmax4-costoffgrid-photovoltaicbatterycost>`


::

    class PhotovoltaicBatteryKilowattHoursPerPhotovoltaicComponentKilowatt(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic battery kilowatt-hours per photovoltaic component kilowatt'
        aliases = ['og_pb_hkw']
        default = 5
        units = 'kilowatt-hours per kilowatt'



.. _mvmax4-costoffgrid-photovoltaicbatterylifetime:

Photovoltaic battery lifetime
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic battery replacement cost per year <mvmax4-costoffgrid-photovoltaicbatteryreplacementcostperyear>`


::

    class PhotovoltaicBatteryLifetime(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic battery lifetime'
        aliases = ['og_pb_life']
        c = dict(check=store.assertPositive)
        default = 3
        units = 'years'



.. _mvmax4-costoffgrid-photovoltaicbatteryreplacementcostperyear:

Photovoltaic battery replacement cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic battery cost <mvmax4-costoffgrid-photovoltaicbatterycost>`

- :ref:`system (off-grid) > photovoltaic battery lifetime <mvmax4-costoffgrid-photovoltaicbatterylifetime>`

Derivatives

- :ref:`system (off-grid) > photovoltaic component recurring cost per year <mvmax4-costoffgrid-photovoltaiccomponentrecurringcostperyear>`


::

    class PhotovoltaicBatteryReplacementCostPerYear(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic battery replacement cost per year'
        aliases = ['og_pb_rep']
        dependencies = [
            PhotovoltaicBatteryCost,
            PhotovoltaicBatteryLifetime,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(PhotovoltaicBatteryCost) / float(self.get(PhotovoltaicBatteryLifetime))



.. _mvmax4-costoffgrid-photovoltaiccomponentefficiencyloss:

Photovoltaic component efficiency loss
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic panel desired capacity <mvmax4-costoffgrid-photovoltaicpaneldesiredsystemcapacity>`


::

    class PhotovoltaicComponentEfficiencyLoss(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic component efficiency loss'
        aliases = ['og_p_loss']
        c = dict(check=store.assertLessThanOne)
        default = 0.1
        units = 'fraction'



.. _mvmax4-costoffgrid-photovoltaiccomponentinitialcost:

Photovoltaic component initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic panel cost <mvmax4-costoffgrid-photovoltaicpanelcost>`

- :ref:`system (off-grid) > photovoltaic battery cost <mvmax4-costoffgrid-photovoltaicbatterycost>`

- :ref:`system (off-grid) > photovoltaic balance cost <mvmax4-costoffgrid-photovoltaicbalancecost>`

Derivatives

- :ref:`system (off-grid) > system initial cost <mvmax4-costoffgrid-offgridsysteminitialcost>`

- :ref:`system (off-grid) > photovoltaic component operations and maintenance cost per year <mvmax4-costoffgrid-photovoltaiccomponentoperationsandmaintenancecostperyear>`


::

    class PhotovoltaicComponentInitialCost(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic component initial cost'
        aliases = ['og_p_ini']
        dependencies = [
            PhotovoltaicPanelCost,
            PhotovoltaicBatteryCost,
            PhotovoltaicBalanceCost,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(PhotovoltaicPanelCost) + self.get(PhotovoltaicBatteryCost) + self.get(PhotovoltaicBalanceCost)



.. _mvmax4-costoffgrid-photovoltaiccomponentoperationsandmaintenancecostperyear:

Photovoltaic component operations and maintenance cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic component operations and maintenance cost per year as fraction of component cost <mvmax4-costoffgrid-photovoltaiccomponentoperationsandmaintenancecostperyearasfractionofcomponentcost>`

- :ref:`system (off-grid) > photovoltaic component initial cost <mvmax4-costoffgrid-photovoltaiccomponentinitialcost>`

Derivatives

- :ref:`system (off-grid) > photovoltaic component recurring cost per year <mvmax4-costoffgrid-photovoltaiccomponentrecurringcostperyear>`


::

    class PhotovoltaicComponentOperationsAndMaintenanceCostPerYear(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic component operations and maintenance cost per year'
        aliases = ['og_p_om']
        dependencies = [
            PhotovoltaicComponentOperationsAndMaintenanceCostPerYearAsFractionOfComponentCost,
            PhotovoltaicComponentInitialCost,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(PhotovoltaicComponentOperationsAndMaintenanceCostPerYearAsFractionOfComponentCost) * self.get(PhotovoltaicComponentInitialCost)



.. _mvmax4-costoffgrid-photovoltaiccomponentoperationsandmaintenancecostperyearasfractionofcomponentcost:

Photovoltaic component operations and maintenance cost per year as fraction of component cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic component operations and maintenance cost per year <mvmax4-costoffgrid-photovoltaiccomponentoperationsandmaintenancecostperyear>`


::

    class PhotovoltaicComponentOperationsAndMaintenanceCostPerYearAsFractionOfComponentCost(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic component operations and maintenance cost per year as fraction of component cost'
        aliases = ['og_p_omf']
        default = 0.05



.. _mvmax4-costoffgrid-photovoltaiccomponentrecurringcostperyear:

Photovoltaic component recurring cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic panel replacement cost per year <mvmax4-costoffgrid-photovoltaicpanelreplacementcostperyear>`

- :ref:`system (off-grid) > photovoltaic battery replacement cost per year <mvmax4-costoffgrid-photovoltaicbatteryreplacementcostperyear>`

- :ref:`system (off-grid) > photovoltaic balance replacement cost per year <mvmax4-costoffgrid-photovoltaicbalancereplacementcostperyear>`

- :ref:`system (off-grid) > photovoltaic component operations and maintenance cost per year <mvmax4-costoffgrid-photovoltaiccomponentoperationsandmaintenancecostperyear>`

Derivatives

- :ref:`system (off-grid) > system recurring cost per year <mvmax4-costoffgrid-offgridsystemrecurringcostperyear>`


::

    class PhotovoltaicComponentRecurringCostPerYear(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic component recurring cost per year'
        aliases = ['og_p_rec']
        dependencies = [
            PhotovoltaicPanelReplacementCostPerYear,
            PhotovoltaicBatteryReplacementCostPerYear,
            PhotovoltaicBalanceReplacementCostPerYear,
            PhotovoltaicComponentOperationsAndMaintenanceCostPerYear,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(PhotovoltaicPanelReplacementCostPerYear) + self.get(PhotovoltaicBatteryReplacementCostPerYear) + self.get(PhotovoltaicBalanceReplacementCostPerYear) + self.get(PhotovoltaicComponentOperationsAndMaintenanceCostPerYear)



.. _mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacity:

Photovoltaic panel actual system capacity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > available system capacities (photovoltaic panel) <mvmax4-costoffgrid-photovoltaicpanelavailablesystemcapacities>`

- :ref:`system (off-grid) > photovoltaic panel actual capacity counts <mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacitycounts>`

Derivatives

- :ref:`system (off-grid) > photovoltaic battery cost <mvmax4-costoffgrid-photovoltaicbatterycost>`

- :ref:`system (off-grid) > photovoltaic panel cost <mvmax4-costoffgrid-photovoltaicpanelcost>`


::

    class PhotovoltaicPanelActualSystemCapacity(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic panel actual capacity'
        aliases = ['og_pp_acp']
        dependencies = [
            PhotovoltaicPanelAvailableSystemCapacities,
            PhotovoltaicPanelActualSystemCapacityCounts,
        ]
        units = 'kilowatts'
    
        def compute(self):
            return numpy.dot(
                self.get(PhotovoltaicPanelAvailableSystemCapacities), 
                self.get(PhotovoltaicPanelActualSystemCapacityCounts))



.. _mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacitycounts:

Photovoltaic panel actual system capacity counts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic panel desired capacity <mvmax4-costoffgrid-photovoltaicpaneldesiredsystemcapacity>`

- :ref:`system (off-grid) > available system capacities (photovoltaic panel) <mvmax4-costoffgrid-photovoltaicpanelavailablesystemcapacities>`

Derivatives

- :ref:`system (off-grid) > photovoltaic panel actual capacity <mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacity>`


::

    class PhotovoltaicPanelActualSystemCapacityCounts(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic panel actual capacity counts'
        aliases = ['og_pp_acps']
        c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
        dependencies = [
            PhotovoltaicPanelDesiredSystemCapacity,
            PhotovoltaicPanelAvailableSystemCapacities,
        ]
        units = 'capacity count list'
    
        def compute(self):
            return metric.computeSystemCounts(
                self.get(PhotovoltaicPanelDesiredSystemCapacity), 
                self.get(PhotovoltaicPanelAvailableSystemCapacities))



.. _mvmax4-costoffgrid-photovoltaicpanelavailablesystemcapacities:

Photovoltaic panel available system capacities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic panel actual capacity <mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacity>`

- :ref:`system (off-grid) > photovoltaic panel actual capacity counts <mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacitycounts>`


::

    class PhotovoltaicPanelAvailableSystemCapacities(V):
    
        section = 'system (off-grid)'
        option = 'available system capacities (photovoltaic panel)'
        aliases = ['og_pp_cps']
        c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
        default = '1.5 1.0 0.4 0.15 0.075 0.05'
        units = 'kilowatts list'



.. _mvmax4-costoffgrid-photovoltaicpanelcost:

Photovoltaic panel cost
^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic panel cost per photovoltaic component kilowatt <mvmax4-costoffgrid-photovoltaicpanelcostperphotovoltaiccomponentkilowatt>`

- :ref:`system (off-grid) > photovoltaic panel actual capacity <mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacity>`

Derivatives

- :ref:`system (off-grid) > photovoltaic balance cost <mvmax4-costoffgrid-photovoltaicbalancecost>`

- :ref:`system (off-grid) > photovoltaic component initial cost <mvmax4-costoffgrid-photovoltaiccomponentinitialcost>`

- :ref:`system (off-grid) > photovoltaic panel replacement cost per year <mvmax4-costoffgrid-photovoltaicpanelreplacementcostperyear>`


::

    class PhotovoltaicPanelCost(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic panel cost'
        aliases = ['og_pp_ini']
        dependencies = [
            PhotovoltaicPanelCostPerPhotovoltaicComponentKilowatt,
            PhotovoltaicPanelActualSystemCapacity,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(PhotovoltaicPanelCostPerPhotovoltaicComponentKilowatt) * self.get(PhotovoltaicPanelActualSystemCapacity)



.. _mvmax4-costoffgrid-photovoltaicpanelcostperphotovoltaiccomponentkilowatt:

Photovoltaic panel cost per photovoltaic component kilowatt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic panel cost <mvmax4-costoffgrid-photovoltaicpanelcost>`


::

    class PhotovoltaicPanelCostPerPhotovoltaicComponentKilowatt(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic panel cost per photovoltaic component kilowatt'
        aliases = ['og_pp_ckw']
        default = 6000
        units = 'dollars per kilowatt'



.. _mvmax4-costoffgrid-photovoltaicpaneldesiredsystemcapacity:

Photovoltaic panel desired system capacity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (household) > projected household demand per year <mvmax4-demand-projectedhouseholddemandperyear>`

- :ref:`demand (social infrastructure) > projected health facility demand per year <mvmax4-demand-projectedhealthfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected education facility demand per year <mvmax4-demand-projectededucationfacilitydemandperyear>`

- :ref:`demand (social infrastructure) > projected public lighting facility demand per year <mvmax4-demand-projectedpubliclightingfacilitydemandperyear>`

- :ref:`system (off-grid) > photovoltaic component efficiency loss <mvmax4-costoffgrid-photovoltaiccomponentefficiencyloss>`

- :ref:`system (off-grid) > peak sun hours per year <mvmax4-costoffgrid-peaksunhoursperyear>`

Derivatives

- :ref:`system (off-grid) > photovoltaic panel actual capacity counts <mvmax4-costoffgrid-photovoltaicpanelactualsystemcapacitycounts>`


::

    class PhotovoltaicPanelDesiredSystemCapacity(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic panel desired capacity'
        aliases = ['og_pp_dcp']
        dependencies = [
            demand.ProjectedHouseholdDemandPerYear,
            demand.ProjectedHealthFacilityDemandPerYear,
            demand.ProjectedEducationFacilityDemandPerYear,
            demand.ProjectedPublicLightingFacilityDemandPerYear,
            PhotovoltaicComponentEfficiencyLoss,
            PeakSunHoursPerYear,
        ]
        units = 'kilowatts'
    
        def compute(self):
            # Computed effectiveDemandPerYear scaled by photovoltaic component loss
            effectiveDemandPerYear = sum([
                self.get(demand.ProjectedHouseholdDemandPerYear),
                self.get(demand.ProjectedHealthFacilityDemandPerYear),
                self.get(demand.ProjectedEducationFacilityDemandPerYear),
                self.get(demand.ProjectedPublicLightingFacilityDemandPerYear),
            ]) / float(1 - self.get(PhotovoltaicComponentEfficiencyLoss))
            # Return
            return effectiveDemandPerYear / float(self.get(PeakSunHoursPerYear))



.. _mvmax4-costoffgrid-photovoltaicpanellifetime:

Photovoltaic panel lifetime
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > photovoltaic panel replacement cost per year <mvmax4-costoffgrid-photovoltaicpanelreplacementcostperyear>`


::

    class PhotovoltaicPanelLifetime(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic panel lifetime'
        aliases = ['og_pp_life']
        c = dict(check=store.assertPositive)
        default = 30
        units = 'years'



.. _mvmax4-costoffgrid-photovoltaicpanelreplacementcostperyear:

Photovoltaic panel replacement cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (off-grid) > photovoltaic panel cost <mvmax4-costoffgrid-photovoltaicpanelcost>`

- :ref:`system (off-grid) > photovoltaic panel lifetime <mvmax4-costoffgrid-photovoltaicpanellifetime>`

Derivatives

- :ref:`system (off-grid) > photovoltaic component recurring cost per year <mvmax4-costoffgrid-photovoltaiccomponentrecurringcostperyear>`


::

    class PhotovoltaicPanelReplacementCostPerYear(V):
    
        section = 'system (off-grid)'
        option = 'photovoltaic panel replacement cost per year'
        aliases = ['og_pp_rep']
        dependencies = [
            PhotovoltaicPanelCost,
            PhotovoltaicPanelLifetime,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(PhotovoltaicPanelCost) / float(self.get(PhotovoltaicPanelLifetime))



System (mini-grid)
------------------

.. _mvmax4-costminigrid-dieselfuelcostperliter:

Diesel fuel cost per liter
^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > diesel fuel cost per year <mvmax4-costminigrid-dieselfuelcostperyear>`

- :ref:`system (off-grid) > diesel fuel cost per year <mvmax4-costoffgrid-dieselfuelcostperyear>`


::

    class DieselFuelCostPerLiter(V):
    
        section = 'system (mini-grid)'
        option = 'diesel fuel cost per liter'
        aliases = ['mg_fl_cl']
        default = 1.08
        units = 'dollars per liter'



.. _mvmax4-costminigrid-dieselfuelcostperyear:

Diesel fuel cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel fuel cost per liter <mvmax4-costminigrid-dieselfuelcostperliter>`

- :ref:`system (mini-grid) > diesel fuel liters consumed per kilowatt-hour <mvmax4-costminigrid-dieselfuellitersconsumedperkilowatthour>`

- :ref:`system (mini-grid) > diesel generator actual system capacity <mvmax4-costminigrid-dieselgeneratoractualsystemcapacity>`

- :ref:`system (mini-grid) > diesel generator hours of operation per year (effective) <mvmax4-costminigrid-dieselgeneratoreffectivehoursofoperationperyear>`

Derivatives

- :ref:`system (mini-grid) > system recurring cost per year <mvmax4-costminigrid-minigridsystemrecurringcostperyear>`


::

    class DieselFuelCostPerYear(V):
    
        section = 'system (mini-grid)'
        option = 'diesel fuel cost per year'
        aliases = ['mg_fl']
        dependencies = [
            DieselFuelCostPerLiter,
            DieselFuelLitersConsumedPerKilowattHour,
            DieselGeneratorActualSystemCapacity,
            DieselGeneratorEffectiveHoursOfOperationPerYear,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(DieselFuelCostPerLiter) * self.get(DieselFuelLitersConsumedPerKilowattHour) * self.get(DieselGeneratorActualSystemCapacity) * self.get(DieselGeneratorEffectiveHoursOfOperationPerYear)



.. _mvmax4-costminigrid-dieselfuellitersconsumedperkilowatthour:

Diesel fuel liters consumed per kilowatt hour
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > diesel fuel cost per year <mvmax4-costminigrid-dieselfuelcostperyear>`

- :ref:`system (off-grid) > diesel fuel cost per year <mvmax4-costoffgrid-dieselfuelcostperyear>`


::

    class DieselFuelLitersConsumedPerKilowattHour(V):
    
        section = 'system (mini-grid)'
        option = 'diesel fuel liters consumed per kilowatt-hour'
        aliases = ['mg_fl_lkwh']
        default = 0.5
        units = 'liters per kilowatt-hour'



.. _mvmax4-costminigrid-dieselgeneratoractualsystemcapacity:

Diesel generator actual system capacity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > available system capacities (diesel generator) <mvmax4-costminigrid-dieselgeneratoravailablesystemcapacities>`

- :ref:`system (mini-grid) > diesel generator actual system capacity counts <mvmax4-costminigrid-dieselgeneratoractualsystemcapacitycounts>`

Derivatives

- :ref:`system (mini-grid) > diesel fuel cost per year <mvmax4-costminigrid-dieselfuelcostperyear>`

- :ref:`system (mini-grid) > diesel generator cost <mvmax4-costminigrid-dieselgeneratorcost>`

- :ref:`system (mini-grid) > diesel generator hours of operation per year (effective) <mvmax4-costminigrid-dieselgeneratoreffectivehoursofoperationperyear>`


::

    class DieselGeneratorActualSystemCapacity(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator actual system capacity'
        aliases = ['mg_dg_acp']
        dependencies = [
            DieselGeneratorAvailableSystemCapacities,
            DieselGeneratorActualSystemCapacityCounts,
        ]
        units = 'kilowatts'
    
        def compute(self):
            return numpy.dot(
                self.get(DieselGeneratorAvailableSystemCapacities), 
                self.get(DieselGeneratorActualSystemCapacityCounts))



.. _mvmax4-costminigrid-dieselgeneratoractualsystemcapacitycounts:

Diesel generator actual system capacity counts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator desired system capacity <mvmax4-costminigrid-dieselgeneratordesiredsystemcapacity>`

- :ref:`system (mini-grid) > available system capacities (diesel generator) <mvmax4-costminigrid-dieselgeneratoravailablesystemcapacities>`

Derivatives

- :ref:`system (mini-grid) > diesel generator actual system capacity <mvmax4-costminigrid-dieselgeneratoractualsystemcapacity>`


::

    class DieselGeneratorActualSystemCapacityCounts(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator actual system capacity counts'
        aliases = ['mg_dg_acps']
        c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
        dependencies = [
            DieselGeneratorDesiredSystemCapacity,
            DieselGeneratorAvailableSystemCapacities,
        ]
        units = 'capacity count list'
    
        def compute(self):
            return metric.computeSystemCounts(
                self.get(DieselGeneratorDesiredSystemCapacity), 
                self.get(DieselGeneratorAvailableSystemCapacities))



.. _mvmax4-costminigrid-dieselgeneratoravailablesystemcapacities:

Diesel generator available system capacities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > diesel generator actual system capacity <mvmax4-costminigrid-dieselgeneratoractualsystemcapacity>`

- :ref:`system (mini-grid) > diesel generator actual system capacity counts <mvmax4-costminigrid-dieselgeneratoractualsystemcapacitycounts>`


::

    class DieselGeneratorAvailableSystemCapacities(V):
    
        section = 'system (mini-grid)'
        option = 'available system capacities (diesel generator)'
        aliases = ['mg_dg_cps']
        c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
        default = '1000 750 500 400 200 150 100 70 32 19 12 6'
        units = 'kilowatts list'



.. _mvmax4-costminigrid-dieselgeneratorcost:

Diesel generator cost
^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator cost per diesel system kilowatt <mvmax4-costminigrid-dieselgeneratorcostperdieselsystemkilowatt>`

- :ref:`system (mini-grid) > diesel generator actual system capacity <mvmax4-costminigrid-dieselgeneratoractualsystemcapacity>`

Derivatives

- :ref:`system (mini-grid) > diesel generator installation cost <mvmax4-costminigrid-dieselgeneratorinstallationcost>`

- :ref:`system (mini-grid) > diesel generator operations and maintenance cost per year <mvmax4-costminigrid-dieselgeneratoroperationsandmaintenancecostperyear>`

- :ref:`system (mini-grid) > diesel generator replacement cost per year <mvmax4-costminigrid-dieselgeneratorreplacementcostperyear>`

- :ref:`system (mini-grid) > system initial cost <mvmax4-costminigrid-minigridsysteminitialcost>`


::

    class DieselGeneratorCost(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator cost'
        aliases = ['mg_dg_ini']
        dependencies = [
            DieselGeneratorCostPerDieselSystemKilowatt,
            DieselGeneratorActualSystemCapacity,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(DieselGeneratorCostPerDieselSystemKilowatt) * self.get(DieselGeneratorActualSystemCapacity)



.. _mvmax4-costminigrid-dieselgeneratorcostperdieselsystemkilowatt:

Diesel generator cost per diesel system kilowatt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > diesel generator cost <mvmax4-costminigrid-dieselgeneratorcost>`

- :ref:`system (off-grid) > diesel generator cost <mvmax4-costoffgrid-dieselgeneratorcost>`


::

    class DieselGeneratorCostPerDieselSystemKilowatt(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator cost per diesel system kilowatt'
        aliases = ['mg_dg_ck']
        default = 150
        units = 'dollars per kilowatt'



.. _mvmax4-costminigrid-dieselgeneratordesiredsystemcapacity:

Diesel generator desired system capacity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (peak) > projected peak nodal demand <mvmax4-demand-projectedpeaknodaldemand>`

- :ref:`system (mini-grid) > distribution loss <mvmax4-costminigrid-distributionloss>`

Derivatives

- :ref:`system (mini-grid) > diesel generator actual system capacity counts <mvmax4-costminigrid-dieselgeneratoractualsystemcapacitycounts>`


::

    class DieselGeneratorDesiredSystemCapacity(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator desired system capacity'
        aliases = ['mg_dg_dcp']
        dependencies = [
            demand.ProjectedPeakNodalDemand,
            DistributionLoss,
        ]
        units = 'kilowatts'
    
        def compute(self):
            return self.get(demand.ProjectedPeakNodalDemand) / float(1 - self.get(DistributionLoss))



.. _mvmax4-costminigrid-dieselgeneratoreffectivehoursofoperationperyear:

Diesel generator effective hours of operation per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`system (mini-grid) > distribution loss <mvmax4-costminigrid-distributionloss>`

- :ref:`system (mini-grid) > diesel generator hours of operation per year (minimum) <mvmax4-costminigrid-dieselgeneratorminimumhoursofoperationperyear>`

- :ref:`system (mini-grid) > diesel generator actual system capacity <mvmax4-costminigrid-dieselgeneratoractualsystemcapacity>`

Derivatives

- :ref:`system (mini-grid) > diesel fuel cost per year <mvmax4-costminigrid-dieselfuelcostperyear>`


::

    class DieselGeneratorEffectiveHoursOfOperationPerYear(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator hours of operation per year (effective)'
        aliases = ['mg_dg_efhr']
        dependencies = [
            demand.ProjectedNodalDemandPerYear,
            DistributionLoss,
            DieselGeneratorMinimumHoursOfOperationPerYear,
            DieselGeneratorActualSystemCapacity,
        ]
        units = 'hours per year'
    
        def compute(self):
            # Initialize
            dieselGeneratorActualSystemCapacity = self.get(DieselGeneratorActualSystemCapacity)
            # If the capacity of the diesel generator is zero,
            if dieselGeneratorActualSystemCapacity == 0:
                # Return zero hours of operation
                return 0
            # Compute effectiveDemandPerYear and assume a mini-grid diesel generator has distribution loss
            effectiveDemandPerYear = self.get(demand.ProjectedNodalDemandPerYear) / float(1 - self.get(DistributionLoss))
            # Return
            return max(self.get(DieselGeneratorMinimumHoursOfOperationPerYear), effectiveDemandPerYear / float(dieselGeneratorActualSystemCapacity))



.. _mvmax4-costminigrid-dieselgeneratorinstallationcost:

Diesel generator installation cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator installation cost as fraction of generator cost <mvmax4-costminigrid-dieselgeneratorinstallationcostasfractionofgeneratorcost>`

- :ref:`system (mini-grid) > diesel generator cost <mvmax4-costminigrid-dieselgeneratorcost>`

Derivatives

- :ref:`system (mini-grid) > system initial cost <mvmax4-costminigrid-minigridsysteminitialcost>`


::

    class DieselGeneratorInstallationCost(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator installation cost'
        aliases = ['mg_dg_i']
        dependencies = [
            DieselGeneratorInstallationCostAsFractionOfGeneratorCost,
            DieselGeneratorCost,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(DieselGeneratorInstallationCostAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)



.. _mvmax4-costminigrid-dieselgeneratorinstallationcostasfractionofgeneratorcost:

Diesel generator installation cost as fraction of generator cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > diesel generator installation cost <mvmax4-costminigrid-dieselgeneratorinstallationcost>`

- :ref:`system (off-grid) > diesel generator installation cost <mvmax4-costoffgrid-dieselgeneratorinstallationcost>`


::

    class DieselGeneratorInstallationCostAsFractionOfGeneratorCost(V):
    
        section = 'system (mini-grid)'
        aliases = ['mg_dg_if']
        option = 'diesel generator installation cost as fraction of generator cost'
        default = 0.25



.. _mvmax4-costminigrid-dieselgeneratorlifetime:

Diesel generator lifetime
^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > diesel generator replacement cost per year <mvmax4-costminigrid-dieselgeneratorreplacementcostperyear>`

- :ref:`system (off-grid) > diesel generator replacement cost per year <mvmax4-costoffgrid-dieselgeneratorreplacementcostperyear>`


::

    class DieselGeneratorLifetime(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator lifetime'
        aliases = ['mg_dg_life']
        c = dict(check=store.assertPositive)
        default = 5
        units = 'years'



.. _mvmax4-costminigrid-dieselgeneratorminimumhoursofoperationperyear:

Diesel generator minimum hours of operation per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > diesel generator hours of operation per year (effective) <mvmax4-costminigrid-dieselgeneratoreffectivehoursofoperationperyear>`


::

    class DieselGeneratorMinimumHoursOfOperationPerYear(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator hours of operation per year (minimum)'
        aliases = ['mg_dg_mnhr']
        default = 1460
        units = 'hours per year'



.. _mvmax4-costminigrid-dieselgeneratoroperationsandmaintenancecostperyear:

Diesel generator operations and maintenance cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator operations and maintenance cost per year as fraction of generator cost <mvmax4-costminigrid-dieselgeneratoroperationsandmaintenancecostperyearasfractionofgeneratorcost>`

- :ref:`system (mini-grid) > diesel generator cost <mvmax4-costminigrid-dieselgeneratorcost>`

Derivatives

- :ref:`system (mini-grid) > system recurring cost per year <mvmax4-costminigrid-minigridsystemrecurringcostperyear>`


::

    class DieselGeneratorOperationsAndMaintenanceCostPerYear(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator operations and maintenance cost per year'
        aliases = ['mg_dg_om']
        dependencies = [
            DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost,
            DieselGeneratorCost,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost) * self.get(DieselGeneratorCost)



.. _mvmax4-costminigrid-dieselgeneratoroperationsandmaintenancecostperyearasfractionofgeneratorcost:

Diesel generator operations and maintenance cost per year as fraction of generator cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (off-grid) > diesel generator operations and maintenance cost per year <mvmax4-costoffgrid-dieselgeneratoroperationsandmaintenancecostperyear>`

- :ref:`system (mini-grid) > diesel generator operations and maintenance cost per year <mvmax4-costminigrid-dieselgeneratoroperationsandmaintenancecostperyear>`


::

    class DieselGeneratorOperationsAndMaintenanceCostPerYearAsFractionOfGeneratorCost(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator operations and maintenance cost per year as fraction of generator cost'
        aliases = ['mg_dg_omf']
        default = 0.01



.. _mvmax4-costminigrid-dieselgeneratorreplacementcostperyear:

Diesel generator replacement cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator cost <mvmax4-costminigrid-dieselgeneratorcost>`

- :ref:`system (mini-grid) > diesel generator lifetime <mvmax4-costminigrid-dieselgeneratorlifetime>`

Derivatives

- :ref:`system (mini-grid) > system recurring cost per year <mvmax4-costminigrid-minigridsystemrecurringcostperyear>`


::

    class DieselGeneratorReplacementCostPerYear(V):
    
        section = 'system (mini-grid)'
        option = 'diesel generator replacement cost per year'
        aliases = ['mg_dg_rep']
        dependencies = [
            DieselGeneratorCost,
            DieselGeneratorLifetime,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(DieselGeneratorCost) / float(self.get(DieselGeneratorLifetime))



.. _mvmax4-costminigrid-distributionloss:

Distribution loss
^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > diesel generator desired system capacity <mvmax4-costminigrid-dieselgeneratordesiredsystemcapacity>`

- :ref:`system (mini-grid) > diesel generator hours of operation per year (effective) <mvmax4-costminigrid-dieselgeneratoreffectivehoursofoperationperyear>`


::

    class DistributionLoss(V):
    
        section = 'system (mini-grid)'
        option = 'distribution loss'
        aliases = ['mg_loss']
        c = dict(check=store.assertLessThanOne)
        default = 0.10
        units = 'fraction'



.. _mvmax4-costminigrid-lowvoltagelineequipmentcost:

Low voltage line equipment cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`distribution > low voltage line equipment cost per connection <mvmax4-costdistribution-lowvoltagelineequipmentcostperconnection>`

- :ref:`demand (household) > target household count <mvmax4-demand-targethouseholdcount>`

Derivatives

- :ref:`system (mini-grid) > low voltage line equipment operations and maintenance cost per year <mvmax4-costminigrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear>`

- :ref:`system (mini-grid) > system initial cost <mvmax4-costminigrid-minigridsysteminitialcost>`


::

    class LowVoltageLineEquipmentCost(V):
    
        section = 'system (mini-grid)'
        option = 'low voltage line equipment cost'
        aliases = ['mg_le']
        dependencies = [
            costDistribution.LowVoltageLineEquipmentCostPerConnection,
            demand.TargetHouseholdCount,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(costDistribution.LowVoltageLineEquipmentCostPerConnection) * self.get(demand.TargetHouseholdCount)



.. _mvmax4-costminigrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear:

Low voltage line equipment operations and maintenance cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`distribution > low voltage line equipment operations and maintenance cost as fraction of equipment cost <mvmax4-costdistribution-lowvoltagelineequipmentoperationsandmaintenancecostperyearasfractionofequipmentcost>`

- :ref:`system (mini-grid) > low voltage line equipment cost <mvmax4-costminigrid-lowvoltagelineequipmentcost>`

Derivatives

- :ref:`system (mini-grid) > system recurring cost per year <mvmax4-costminigrid-minigridsystemrecurringcostperyear>`


::

    class LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear(V):
    
        section = 'system (mini-grid)'
        option = 'low voltage line equipment operations and maintenance cost per year'
        aliases = ['mg_le_om']
        dependencies = [
            costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost,
            LowVoltageLineEquipmentCost,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost) * self.get(LowVoltageLineEquipmentCost)



.. _mvmax4-costminigrid-minigridsysteminitialcost:

Mini grid system initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator cost <mvmax4-costminigrid-dieselgeneratorcost>`

- :ref:`system (mini-grid) > diesel generator installation cost <mvmax4-costminigrid-dieselgeneratorinstallationcost>`

- :ref:`system (mini-grid) > low voltage line equipment cost <mvmax4-costminigrid-lowvoltagelineequipmentcost>`

- :ref:`distribution > low voltage line initial cost <mvmax4-costdistribution-lowvoltagelineinitialcost>`

Derivatives

- :ref:`system (mini-grid) > system nodal discounted cost <mvmax4-costminigrid-minigridsystemnodaldiscountedcost>`


::

    class MiniGridSystemInitialCost(V):
    
        section = 'system (mini-grid)'
        option = 'system initial cost'
        aliases = ['mg_ini']
        dependencies = [
            DieselGeneratorCost,
            DieselGeneratorInstallationCost,
            LowVoltageLineEquipmentCost,
            costDistribution.LowVoltageLineInitialCost,
        ]
        units = 'dollars'
    
        def compute(self):
            return sum([
                self.get(DieselGeneratorCost),
                self.get(DieselGeneratorInstallationCost),
                self.get(LowVoltageLineEquipmentCost),
                self.get(costDistribution.LowVoltageLineInitialCost),
            ])



.. _mvmax4-costminigrid-minigridsystemnodaldiscountedcost:

Mini grid system nodal discounted cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`system (mini-grid) > system initial cost <mvmax4-costminigrid-minigridsysteminitialcost>`

- :ref:`system (mini-grid) > system recurring cost per year <mvmax4-costminigrid-minigridsystemrecurringcostperyear>`

- :ref:`finance > discounted cash flow factor <mvmax4-finance-discountedcashflowfactor>`

Derivatives

- :ref:`metric > maximum length of medium voltage line extension <mvmax4-metric>`

- :ref:`system (mini-grid) > system nodal levelized cost <mvmax4-costminigrid-minigridsystemnodallevelizedcost>`

- :ref:`metric > system <mvmax4-system>`


::

    class MiniGridSystemNodalDiscountedCost(V):
    
        section = 'system (mini-grid)'
        option = 'system nodal discounted cost'
        aliases = ['mg_nod_d']
        dependencies = [
            demand.ProjectedNodalDemandPerYear,
            MiniGridSystemInitialCost,
            MiniGridSystemRecurringCostPerYear,
            finance.DiscountedCashFlowFactor,
        ]
        units = 'dollars'
    
        def compute(self):
            if self.get(demand.ProjectedNodalDemandPerYear) == 0:
                return 0
            return self.get(MiniGridSystemInitialCost) + self.get(MiniGridSystemRecurringCostPerYear) * self.get(finance.DiscountedCashFlowFactor)



.. _mvmax4-costminigrid-minigridsystemnodallevelizedcost:

Mini grid system nodal levelized cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand > projected nodal discounted demand <mvmax4-demand-projectednodaldiscounteddemand>`

- :ref:`system (mini-grid) > system nodal discounted cost <mvmax4-costminigrid-minigridsystemnodaldiscountedcost>`

Derivatives

- :ref:`metric > maximum length of medium voltage line extension <mvmax4-metric>`


::

    class MiniGridSystemNodalLevelizedCost(V):
    
        section = 'system (mini-grid)'
        option = 'system nodal levelized cost'
        aliases = ['mg_nod_lev']
        dependencies = [
            demand.ProjectedNodalDiscountedDemand,
            MiniGridSystemNodalDiscountedCost,
        ]
        units = 'dollars per kilowatt-hour'
    
        def compute(self):
            if self.get(demand.ProjectedNodalDiscountedDemand) == 0:
                return 0
            return self.get(MiniGridSystemNodalDiscountedCost) / float(self.get(demand.ProjectedNodalDiscountedDemand))



.. _mvmax4-costminigrid-minigridsystemrecurringcostperyear:

Mini grid system recurring cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > diesel generator operations and maintenance cost per year <mvmax4-costminigrid-dieselgeneratoroperationsandmaintenancecostperyear>`

- :ref:`system (mini-grid) > diesel generator replacement cost per year <mvmax4-costminigrid-dieselgeneratorreplacementcostperyear>`

- :ref:`system (mini-grid) > diesel fuel cost per year <mvmax4-costminigrid-dieselfuelcostperyear>`

- :ref:`system (mini-grid) > low voltage line equipment operations and maintenance cost per year <mvmax4-costminigrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear>`

- :ref:`distribution > low voltage line recurring cost per year <mvmax4-costdistribution-lowvoltagelinerecurringcostperyear>`

Derivatives

- :ref:`system (mini-grid) > system nodal discounted cost <mvmax4-costminigrid-minigridsystemnodaldiscountedcost>`


::

    class MiniGridSystemRecurringCostPerYear(V):
    
        section = 'system (mini-grid)'
        option = 'system recurring cost per year'
        aliases = ['mg_rec']
        dependencies = [
            DieselGeneratorOperationsAndMaintenanceCostPerYear,
            DieselGeneratorReplacementCostPerYear,
            DieselFuelCostPerYear,
            LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear,
            costDistribution.LowVoltageLineRecurringCostPerYear,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return sum([
                self.get(DieselGeneratorOperationsAndMaintenanceCostPerYear),
                self.get(DieselGeneratorReplacementCostPerYear),
                self.get(DieselFuelCostPerYear),
                self.get(LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear),
                self.get(costDistribution.LowVoltageLineRecurringCostPerYear),
            ])



.. _mvmax4-minigridsystemtotal:

Mini grid system total
^^^^^^^^^^^^^^^^^^^^^^


::

    class MiniGridSystemTotal(V):
    
        section = 'system (mini-grid)'
        option = 'system total'
        aliases = ['mg_ct']
        default = 0
        units = 'count'
    
        def aggregate(self, childVS):
            # If the system is mini-grid,
            if childVS.get(System)[0] == 'm':
                # Update
                self.value += 1



.. _mvmax4-minigridsystemtotaldiscountedcost:

Mini grid system total discounted cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > system total levelized cost <mvmax4-minigridsystemtotallevelizedcost>`


::

    class MiniGridSystemTotalDiscountedCost(V):
    
        section = 'system (mini-grid)'
        option = 'system total discounted cost'
        aliases = ['mg_tot_d']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # If the system is mini-grid,
            if childVS.get(System)[0] == 'm':
                # Update
                self.value += childVS.get(costMiniGrid.MiniGridSystemNodalDiscountedCost)



.. _mvmax4-minigridsystemtotaldiscounteddemand:

Mini grid system total discounted demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (mini-grid) > system total levelized cost <mvmax4-minigridsystemtotallevelizedcost>`


::

    class MiniGridSystemTotalDiscountedDemand(V):
    
        section = 'system (mini-grid)'
        option = 'system total discounted demand'
        aliases = ['mg_dem_d']
        default = 0
        units = 'kilowatt-hours'
    
        def aggregate(self, childVS):
            # If the system is mini-grid,
            if childVS.get(System)[0] == 'm':
                # Update
                self.value += childVS.get(demand.ProjectedNodalDiscountedDemand)



.. _mvmax4-minigridsystemtotaldiscounteddieselfuelcost:

Mini grid system total discounted diesel fuel cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


::

    class MiniGridSystemTotalDiscountedDieselFuelCost(V):
    
        section = 'system (mini-grid)'
        option = 'system total discounted diesel fuel cost'
        aliases = ['mg_tot_ddfc']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # If the system is mini-grid,
            if childVS.get(System)[0] == 'm':
                # add up nodal diesel costs
                self.value += childVS.get(costMiniGrid.MiniGridSystemNodalDiscountedDieselFuelCost) 



.. _mvmax4-minigridsystemtotaldiscountedrecurringcost:

Mini grid system total discounted recurring cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


::

    class MiniGridSystemTotalDiscountedRecurringCost(V):
    
        section = 'system (mini-grid)'
        option = 'system total discounted recurring cost'
        aliases = ['mg_tot_drc']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # If the system is mini-grid,
            if childVS.get(System)[0] == 'm':
                # Update
                self.value += ( \
                        childVS.get(costMiniGrid.MiniGridSystemRecurringCostPerYear) * \
                        childVS.get(finance.DiscountedCashFlowFactor))



.. _mvmax4-minigridsystemtotalinitialcost:

Mini grid system total initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


::

    class MiniGridSystemTotalInitialCost(V):
    
        section = 'system (mini-grid)'
        option = 'system total initial cost'
        aliases = ['mg_tot_i']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # If the system is mini-grid,
            if childVS.get(System)[0] == 'm':
                # Update
                self.value += childVS.get(costMiniGrid.MiniGridSystemInitialCost)



.. _mvmax4-minigridsystemtotallevelizedcost:

Mini grid system total levelized cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (mini-grid) > system total discounted demand <mvmax4-minigridsystemtotaldiscounteddemand>`

- :ref:`system (mini-grid) > system total discounted cost <mvmax4-minigridsystemtotaldiscountedcost>`


::

    class MiniGridSystemTotalLevelizedCost(V):
    
        section = 'system (mini-grid)'
        option = 'system total levelized cost'
        aliases = ['mg_tot_lev']
        dependencies = [
            MiniGridSystemTotalDiscountedDemand,
            MiniGridSystemTotalDiscountedCost,
        ]
        units = 'dollars per kilowatt-hour'
    
        def compute(self):
            if self.get(MiniGridSystemTotalDiscountedDemand) == 0:
                return 0
            return self.get(MiniGridSystemTotalDiscountedCost) / float(self.get(MiniGridSystemTotalDiscountedDemand))



System (grid)
-------------

.. _mvmax4-costgrid-distributionloss:

Distribution loss
^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > electricity cost per year <mvmax4-costgrid-gridelectricitycostperyear>`

- :ref:`system (grid) > grid transformer desired system capacity <mvmax4-costgrid-gridtransformerdesiredsystemcapacity>`


::

    class DistributionLoss(V):
    
        section = 'system (grid)'
        option = 'distribution loss'
        aliases = ['gr_loss']
        c = dict(check=store.assertLessThanOne)
        default = 0.15
        units = 'fraction'



.. _mvmax4-costgrid-gridelectricitycostperkilowatthour:

Grid electricity cost per kilowatt hour
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > electricity cost per year <mvmax4-costgrid-gridelectricitycostperyear>`


::

    class GridElectricityCostPerKilowattHour(V):
    
        section = 'system (grid)'
        option = 'electricity cost per kilowatt-hour'
        aliases = ['gr_el_ckwh']
        default = 0.17
        units = 'dollars per kilowatt-hour'



.. _mvmax4-costgrid-gridelectricitycostperyear:

Grid electricity cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > electricity cost per kilowatt-hour <mvmax4-costgrid-gridelectricitycostperkilowatthour>`

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`system (grid) > distribution loss <mvmax4-costgrid-distributionloss>`

Derivatives

- :ref:`system (grid) > internal system recurring cost per year <mvmax4-costgrid-gridinternalsystemrecurringcostperyear>`


::

    class GridElectricityCostPerYear(V):
    
        section = 'system (grid)'
        option = 'electricity cost per year'
        aliases = ['gr_el']
        dependencies = [
            GridElectricityCostPerKilowattHour,
            demand.ProjectedNodalDemandPerYear,
            DistributionLoss,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(GridElectricityCostPerKilowattHour) * self.get(demand.ProjectedNodalDemandPerYear) / float(1 - self.get(DistributionLoss))



.. _mvmax4-costgrid-gridexternalsysteminitialcostpermeter:

Grid external system initial cost per meter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > medium voltage line cost per meter <mvmax4-costgrid-gridmediumvoltagelinecostpermeter>`

Derivatives

- :ref:`system (grid) > external nodal discounted cost per meter <mvmax4-costgrid-gridexternalsystemnodaldiscountedcostpermeter>`


::

    class GridExternalSystemInitialCostPerMeter(V):
    
        section = 'system (grid)'
        option = 'external system initial cost per meter'
        aliases = ['ge_inim']
        dependencies = [
            GridMediumVoltageLineCostPerMeter,
        ]
        units = 'dollars per meter'
    
        def compute(self):
            return self.get(GridMediumVoltageLineCostPerMeter)



.. _mvmax4-costgrid-gridexternalsystemnodaldiscountedcostpermeter:

Grid external system nodal discounted cost per meter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > external system initial cost per meter <mvmax4-costgrid-gridexternalsysteminitialcostpermeter>`

- :ref:`system (grid) > external nodal discounted recurring cost per meter <mvmax4-costgrid-gridexternalsystemnodaldiscountedrecurringcostpermeter>`

Derivatives

- :ref:`metric > maximum length of medium voltage line extension <mvmax4-metric>`


::

    class GridExternalSystemNodalDiscountedCostPerMeter(V):
    
        section = 'system (grid)'
        option = 'external nodal discounted cost per meter'
        aliases = ['ge_nodm_d']
        c = dict(check=store.assertPositive)
        dependencies = [
            GridExternalSystemInitialCostPerMeter,
            GridExternalSystemNodalDiscountedRecurringCostPerMeter,
        ]
        units = 'dollars per meter'
    
        def compute(self):
            return self.get(GridExternalSystemInitialCostPerMeter) + self.get(GridExternalSystemNodalDiscountedRecurringCostPerMeter)



.. _mvmax4-costgrid-gridexternalsystemnodaldiscountedrecurringcostpermeter:

Grid external system nodal discounted recurring cost per meter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > external system recurring cost per meter per year <mvmax4-costgrid-gridexternalsystemrecurringcostpermeterperyear>`

- :ref:`finance > discounted cash flow factor <mvmax4-finance-discountedcashflowfactor>`

Derivatives

- :ref:`system (grid) > external nodal discounted cost per meter <mvmax4-costgrid-gridexternalsystemnodaldiscountedcostpermeter>`


::

    class GridExternalSystemNodalDiscountedRecurringCostPerMeter(V):
    
        section = 'system (grid)'
        option = 'external nodal discounted recurring cost per meter'
        aliases = ['ge_nodm_drcpm']
        c = dict(check=store.assertPositive)
        dependencies = [
            GridExternalSystemRecurringCostPerMeterPerYear,
            finance.DiscountedCashFlowFactor,
        ]
        units = 'dollars per meter'
    
        def compute(self):
            return self.get(GridExternalSystemRecurringCostPerMeterPerYear) * self.get(finance.DiscountedCashFlowFactor)



.. _mvmax4-costgrid-gridexternalsystemrecurringcostpermeterperyear:

Grid external system recurring cost per meter per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > medium voltage line operations and maintenace cost per meter per year <mvmax4-costgrid-gridmediumvoltagelineoperationsandmaintenancecostpermeterperyear>`

- :ref:`system (grid) > medium voltage line replacement cost per meter per year <mvmax4-costgrid-gridmediumvoltagelinereplacementcostpermeterperyear>`

Derivatives

- :ref:`system (grid) > external nodal discounted recurring cost per meter <mvmax4-costgrid-gridexternalsystemnodaldiscountedrecurringcostpermeter>`


::

    class GridExternalSystemRecurringCostPerMeterPerYear(V):
    
        section = 'system (grid)'
        option = 'external system recurring cost per meter per year'
        aliases = ['ge_recm']
        dependencies = [
            GridMediumVoltageLineOperationsAndMaintenanceCostPerMeterPerYear,
            GridMediumVoltageLineReplacementCostPerMeterPerYear,
        ]
        units = 'dollars per meter per year'
    
        def compute(self):
            return self.get(GridMediumVoltageLineOperationsAndMaintenanceCostPerMeterPerYear) + self.get(GridMediumVoltageLineReplacementCostPerMeterPerYear)



.. _mvmax4-costgrid-gridinstallationcost:

Grid installation cost
^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > installation cost per connection <mvmax4-costgrid-gridinstallationcostperconnection>`

- :ref:`system (grid) > internal connection count <mvmax4-costgrid-gridinternalconnectioncount>`

Derivatives

- :ref:`system (grid) > internal system initial cost <mvmax4-costgrid-gridinternalsysteminitialcost>`


::

    class GridInstallationCost(V):
    
        section = 'system (grid)'
        option = 'installation cost'
        aliases = ['gr_i']
        dependencies = [
            GridInstallationCostPerConnection,
            GridInternalConnectionCount,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(GridInstallationCostPerConnection) * self.get(GridInternalConnectionCount) 



.. _mvmax4-costgrid-gridinstallationcostperconnection:

Grid installation cost per connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > installation cost <mvmax4-costgrid-gridinstallationcost>`


::

    class GridInstallationCostPerConnection(V):
    
        section = 'system (grid)'
        option = 'installation cost per connection'
        aliases = ['gr_i_cc']
        default = 130
        units = 'dollars per connection'



.. _mvmax4-costgrid-gridinternalconnectioncount:

Grid internal connection count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (household) > target household count <mvmax4-demand-targethouseholdcount>`

- :ref:`system (grid) > social infrastructure count <mvmax4-costgrid-gridsocialinfrastructurecount>`

Derivatives

- :ref:`system (grid) > installation cost <mvmax4-costgrid-gridinstallationcost>`

- :ref:`system (grid) > low voltage line equipment cost <mvmax4-costgrid-lowvoltagelineequipmentcost>`


::

    class GridInternalConnectionCount(V):
        
        section = 'system (grid)'
        option = 'internal connection count'
        aliases = ['gr_ic']
        dependencies = [
            demand.TargetHouseholdCount,
            GridSocialInfrastructureCount,
        ]
        units = 'connection count'
       
        def compute(self):
            return self.get(demand.TargetHouseholdCount) + self.get(GridSocialInfrastructureCount)



.. _mvmax4-costgrid-gridinternalsysteminitialcost:

Grid internal system initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > installation cost <mvmax4-costgrid-gridinstallationcost>`

- :ref:`system (grid) > transformer cost <mvmax4-costgrid-gridtransformercost>`

- :ref:`system (grid) > low voltage line equipment cost <mvmax4-costgrid-lowvoltagelineequipmentcost>`

- :ref:`distribution > low voltage line initial cost <mvmax4-costdistribution-lowvoltagelineinitialcost>`

Derivatives

- :ref:`system (grid) > internal system nodal discounted cost <mvmax4-costgrid-gridinternalsystemnodaldiscountedcost>`


::

    class GridInternalSystemInitialCost(V):
    
        section = 'system (grid)'
        option = 'internal system initial cost'
        aliases = ['gi_ini']
        dependencies = [
            GridInstallationCost,
            GridTransformerCost,
            LowVoltageLineEquipmentCost,
            costDistribution.LowVoltageLineInitialCost,
        ]
        units = 'dollars'
    
        def compute(self):
            return sum([
                self.get(GridInstallationCost),
                self.get(GridTransformerCost),
                self.get(LowVoltageLineEquipmentCost),
                self.get(costDistribution.LowVoltageLineInitialCost),
            ])



.. _mvmax4-costgrid-gridinternalsystemnodaldiscountedcost:

Grid internal system nodal discounted cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`system (grid) > internal system initial cost <mvmax4-costgrid-gridinternalsysteminitialcost>`

- :ref:`system (grid) > internal system recurring cost per year <mvmax4-costgrid-gridinternalsystemrecurringcostperyear>`

- :ref:`finance > discounted cash flow factor <mvmax4-finance-discountedcashflowfactor>`

Derivatives

- :ref:`system (grid) > internal system nodal levelized cost <mvmax4-costgrid-gridinternalsystemnodallevelizedcost>`

- :ref:`metric > maximum length of medium voltage line extension <mvmax4-metric>`


::

    class GridInternalSystemNodalDiscountedCost(V):
    
        section = 'system (grid)'
        option = 'internal system nodal discounted cost'
        aliases = ['gi_nod_d']
        dependencies = [
            demand.ProjectedNodalDemandPerYear,
            GridInternalSystemInitialCost,
            GridInternalSystemRecurringCostPerYear,
            finance.DiscountedCashFlowFactor,
        ]
        units = 'dollars'
    
        def compute(self):
            if self.get(demand.ProjectedNodalDemandPerYear) == 0:
                return 0
            return self.get(GridInternalSystemInitialCost) + self.get(GridInternalSystemRecurringCostPerYear) * self.get(finance.DiscountedCashFlowFactor)



.. _mvmax4-costgrid-gridinternalsystemnodallevelizedcost:

Grid internal system nodal levelized cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand > projected nodal discounted demand <mvmax4-demand-projectednodaldiscounteddemand>`

- :ref:`system (grid) > internal system nodal discounted cost <mvmax4-costgrid-gridinternalsystemnodaldiscountedcost>`

Derivatives

- :ref:`metric > maximum length of medium voltage line extension <mvmax4-metric>`


::

    class GridInternalSystemNodalLevelizedCost(V):
    
        section = 'system (grid)'
        option = 'internal system nodal levelized cost'
        aliases = ['gi_nod_lev']
        dependencies = [
            demand.ProjectedNodalDiscountedDemand,
            GridInternalSystemNodalDiscountedCost,
        ]
        units = 'dollars per kilowatt-hour'
    
        def compute(self):
            if self.get(demand.ProjectedNodalDiscountedDemand) == 0:
                return 0
            return self.get(GridInternalSystemNodalDiscountedCost) / float(self.get(demand.ProjectedNodalDiscountedDemand))



.. _mvmax4-costgrid-gridinternalsystemrecurringcostperyear:

Grid internal system recurring cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > transformer operations and maintenance cost per year <mvmax4-costgrid-gridtransformeroperationsandmaintenancecostperyear>`

- :ref:`system (grid) > transformer replacement cost per year <mvmax4-costgrid-gridtransformerreplacementcostperyear>`

- :ref:`system (grid) > electricity cost per year <mvmax4-costgrid-gridelectricitycostperyear>`

- :ref:`system (grid) > low voltage line equipment operations and maintenance cost per year <mvmax4-costgrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear>`

- :ref:`distribution > low voltage line recurring cost per year <mvmax4-costdistribution-lowvoltagelinerecurringcostperyear>`

Derivatives

- :ref:`system (grid) > internal system nodal discounted cost <mvmax4-costgrid-gridinternalsystemnodaldiscountedcost>`


::

    class GridInternalSystemRecurringCostPerYear(V):
    
        section = 'system (grid)'
        option = 'internal system recurring cost per year'
        aliases = ['gi_rec']
        dependencies = [
            GridTransformerOperationsAndMaintenanceCostPerYear,
            GridTransformerReplacementCostPerYear,
            GridElectricityCostPerYear,
            LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear,
            costDistribution.LowVoltageLineRecurringCostPerYear,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return sum([
                self.get(GridTransformerOperationsAndMaintenanceCostPerYear),
                self.get(GridTransformerReplacementCostPerYear),
                self.get(GridElectricityCostPerYear),
                self.get(LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear),
                self.get(costDistribution.LowVoltageLineRecurringCostPerYear),
            ])



.. _mvmax4-costgrid-gridmediumvoltagelinecostpermeter:

Grid medium voltage line cost per meter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > external system initial cost per meter <mvmax4-costgrid-gridexternalsysteminitialcostpermeter>`

- :ref:`system (grid) > medium voltage line operations and maintenace cost per meter per year <mvmax4-costgrid-gridmediumvoltagelineoperationsandmaintenancecostpermeterperyear>`

- :ref:`system (grid) > medium voltage line replacement cost per meter per year <mvmax4-costgrid-gridmediumvoltagelinereplacementcostpermeterperyear>`


::

    class GridMediumVoltageLineCostPerMeter(V):
    
        section = 'system (grid)'
        option = 'medium voltage line cost per meter'
        aliases = ['gr_ml_cm']
        default = 20
        units = 'dollars per meter'



.. _mvmax4-costgrid-gridmediumvoltagelinelifetime:

Grid medium voltage line lifetime
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > medium voltage line replacement cost per meter per year <mvmax4-costgrid-gridmediumvoltagelinereplacementcostpermeterperyear>`


::

    class GridMediumVoltageLineLifetime(V):
    
        section = 'system (grid)'
        option = 'medium voltage line lifetime'
        aliases = ['gr_ml_life']
        c = dict(check=store.assertPositive)
        default = 30
        units = 'years'



.. _mvmax4-costgrid-gridmediumvoltagelineoperationsandmaintenancecostpermeterperyear:

Grid medium voltage line operations and maintenance cost per meter per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > medium voltage line operations and maintenance cost per year as fraction of line cost <mvmax4-costgrid-gridmediumvoltagelineoperationsandmaintenancecostperyearasfractionoflinecost>`

- :ref:`system (grid) > medium voltage line cost per meter <mvmax4-costgrid-gridmediumvoltagelinecostpermeter>`

Derivatives

- :ref:`system (grid) > external system recurring cost per meter per year <mvmax4-costgrid-gridexternalsystemrecurringcostpermeterperyear>`


::

    class GridMediumVoltageLineOperationsAndMaintenanceCostPerMeterPerYear(V):
    
        section = 'system (grid)'
        option = 'medium voltage line operations and maintenace cost per meter per year'
        aliases = ['gr_ml_omm']
        dependencies = [
            GridMediumVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost,
            GridMediumVoltageLineCostPerMeter,
        ]
        units = 'dollars per meter per year'
    
        def compute(self):
            return self.get(GridMediumVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost) * self.get(GridMediumVoltageLineCostPerMeter)



.. _mvmax4-costgrid-gridmediumvoltagelineoperationsandmaintenancecostperyearasfractionoflinecost:

Grid medium voltage line operations and maintenance cost per year as fraction of line cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > medium voltage line operations and maintenace cost per meter per year <mvmax4-costgrid-gridmediumvoltagelineoperationsandmaintenancecostpermeterperyear>`


::

    class GridMediumVoltageLineOperationsAndMaintenanceCostPerYearAsFractionOfLineCost(V):
    
        section = 'system (grid)'
        option = 'medium voltage line operations and maintenance cost per year as fraction of line cost'
        aliases = ['gr_ml_omf']
        default = 0.01



.. _mvmax4-costgrid-gridmediumvoltagelinereplacementcostpermeterperyear:

Grid medium voltage line replacement cost per meter per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > medium voltage line cost per meter <mvmax4-costgrid-gridmediumvoltagelinecostpermeter>`

- :ref:`system (grid) > medium voltage line lifetime <mvmax4-costgrid-gridmediumvoltagelinelifetime>`

Derivatives

- :ref:`system (grid) > external system recurring cost per meter per year <mvmax4-costgrid-gridexternalsystemrecurringcostpermeterperyear>`


::

    class GridMediumVoltageLineReplacementCostPerMeterPerYear(V):
    
        section = 'system (grid)'
        option = 'medium voltage line replacement cost per meter per year'
        aliases = ['gr_ml_repm']
        dependencies = [
            GridMediumVoltageLineCostPerMeter,
            GridMediumVoltageLineLifetime,
        ]
        units = 'dollars per meter per year'
    
        def compute(self):
            return self.get(GridMediumVoltageLineCostPerMeter) / float(self.get(GridMediumVoltageLineLifetime))



.. _mvmax4-costgrid-gridsocialinfrastructurecount:

Grid social infrastructure count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (social infrastructure) > projected health facility count <mvmax4-demand-projectedhealthfacilitycount>`

- :ref:`demand (social infrastructure) > projected education facility count <mvmax4-demand-projectededucationfacilitycount>`

- :ref:`demand (social infrastructure) > projected public lighting facility count <mvmax4-demand-projectedpubliclightingfacilitycount>`

- :ref:`demand (social infrastructure) > projected commercial facility count <mvmax4-demand-projectedcommercialfacilitycount>`

Derivatives

- :ref:`system (grid) > internal connection count <mvmax4-costgrid-gridinternalconnectioncount>`


::

    class GridSocialInfrastructureCount(V):
        
        section = 'system (grid)'
        option = 'social infrastructure count'
        aliases = ['gr_so']
        dependencies = [
            demand.ProjectedHealthFacilityCount,
            demand.ProjectedEducationFacilityCount,
            demand.ProjectedPublicLightingFacilityCount,
            demand.ProjectedCommercialFacilityCount,
        ]
        units = 'facility count'
       
        def compute(self):
            return self.get(demand.ProjectedHealthFacilityCount) + self.get(demand.ProjectedEducationFacilityCount) + self.get(demand.ProjectedPublicLightingFacilityCount) + self.get(demand.ProjectedCommercialFacilityCount)



.. _mvmax4-gridsystemtotal:

Grid system total
^^^^^^^^^^^^^^^^^


::

    class GridSystemTotal(V):
    
        section = 'system (grid)'
        option = 'system total'
        aliases = ['g_ct']
        default = 0
        units = 'count'
    
        def aggregate(self, childVS):
            # If the system is grid,
            if childVS.get(System)[0] == 'g':
                # Update
                self.value += 1



.. _mvmax4-gridsystemtotaldiscountedcost:

Grid system total discounted cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > system total levelized cost <mvmax4-gridsystemtotallevelizedcost>`


::

    class GridSystemTotalDiscountedCost(V):
    
        section = 'system (grid)'
        option = 'system total discounted cost'
        aliases = ['gr_tot_d']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # Get
            childDataset = childVS.state[0]
            childNode = childVS.state[1]
            # If the system is grid and we are connecting a node that was not in the existing grid,
            if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
                # Get internal cost
                internalCost = childVS.get(costGrid.GridInternalSystemNodalDiscountedCost)
                # Get half the length of all new connections to the node
                newConnections = childDataset.cycleConnections(childNode, is_existing=False)
                newConnectionLengthHalved = sum(x.weight for x in newConnections) / 2.
                # Get external cost
                externalCostPerMeter = childVS.get(costGrid.GridExternalSystemNodalDiscountedCostPerMeter)
                externalCost = externalCostPerMeter * newConnectionLengthHalved
                # Add internal and external cost
                self.value += internalCost + externalCost



.. _mvmax4-gridsystemtotaldiscounteddemand:

Grid system total discounted demand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > system total levelized cost <mvmax4-gridsystemtotallevelizedcost>`


::

    class GridSystemTotalDiscountedDemand(V):
    
        section = 'system (grid)'
        option = 'system total discounted demand'
        aliases = ['gr_dem_d']
        default = 0
        units = 'kilowatt-hours'
    
        def aggregate(self, childVS):
            # Get
            childDataset = childVS.state[0]
            childNode = childVS.state[1]
            # If the system is grid and we are connecting a node that was not in the existing grid,
            if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
                # Update
                self.value += childVS.get(demand.ProjectedNodalDiscountedDemand)



.. _mvmax4-gridsystemtotaldiscountedrecurringcost:

Grid system total discounted recurring cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > system total external discounted recurring cost <mvmax4-gridsystemtotalexternaldiscountedrecurringcost>`

- :ref:`system (grid) > system total internal discounted recurring cost <mvmax4-gridsystemtotalinternaldiscountedrecurringcost>`


::

    class GridSystemTotalDiscountedRecurringCost(V):
    
        section = 'system (grid)'
        option = 'system total discounted recurring cost'
        aliases = ['gr_tot_drc']
        dependencies = [
            GridSystemTotalExternalDiscountedRecurringCost,
            GridSystemTotalInternalDiscountedRecurringCost,
        ]
        units = 'dollars'
    
        def compute(self):
            # Sum internal and external recurring costs and apply discounted cash flow factor
            intlCostPerYear = self.get(GridSystemTotalExternalDiscountedRecurringCost)
            extlCostPerYear = self.get(GridSystemTotalInternalDiscountedRecurringCost)
            return (intlCostPerYear + extlCostPerYear)



.. _mvmax4-gridsystemtotalexistingnetworklength:

Grid system total existing network length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`metric > system <mvmax4-system>`


::

    class GridSystemTotalExistingNetworkLength(V):
    
        section = 'system (grid)'
        option = 'system total existing network length'
        aliases = ['gr_tot_enl']
        units = 'meters'
    
        # Don't understand why we need this
        dependencies = [System]
    
        def compute(self):
            return self.state[0].sumNetworkWeight(is_existing=True)



.. _mvmax4-gridsystemtotalexternaldiscountedrecurringcost:

Grid system total external discounted recurring cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > system total discounted recurring cost <mvmax4-gridsystemtotaldiscountedrecurringcost>`


::

    class GridSystemTotalExternalDiscountedRecurringCost(V):
    
        section = 'system (grid)'
        option = 'system total external discounted recurring cost'
        aliases = ['gr_tot_ext_drc']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # Get
            childDataset = childVS.state[0]
            childNode = childVS.state[1]
            # If the system is grid and we are connecting a node that was not in the existing grid,
            if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
                # Get half the length of all new connections to the node
                newConnections = childDataset.cycleConnections(childNode, is_existing=False)
                newConnectionLengthHalved = sum(x.weight for x in newConnections) / 2.
                # Get discounted external cost
                discountedExternalCostPerMeter = childVS.get(costGrid.GridExternalSystemNodalDiscountedRecurringCostPerMeter)
                externalRecurringCost = discountedExternalCostPerMeter * newConnectionLengthHalved
                self.value += externalRecurringCost



.. _mvmax4-gridsystemtotalexternalinitialcost:

Grid system total external initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > system total initial cost <mvmax4-gridsystemtotalinitialcost>`


::

    class GridSystemTotalExternalInitialCost(V):
    
        section = 'system (grid)'
        option = 'system total external initial cost'
        aliases = ['gr_tot_ext_ic']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # Get
            childDataset = childVS.state[0]
            childNode = childVS.state[1]
            # If the system is grid and we are connecting a node that was not in the existing grid,
            if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
                # Get half the length of all new connections to the node
                newConnections = childDataset.cycleConnections(childNode, is_existing=False)
                newConnectionLengthHalved = sum(x.weight for x in newConnections) / 2.
                # Get initial external cost
                externalCostPerMeter = childVS.get(costGrid.GridExternalSystemInitialCostPerMeter)
                externalCost = externalCostPerMeter * newConnectionLengthHalved
                # Add internal and external cost
                self.value += externalCost



.. _mvmax4-gridsystemtotalinitialcost:

Grid system total initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > system total internal initial cost <mvmax4-gridsystemtotalinternalinitialcost>`

- :ref:`system (grid) > system total external initial cost <mvmax4-gridsystemtotalexternalinitialcost>`


::

    class GridSystemTotalInitialCost(V):
    
        section = 'system (grid)'
        option = 'system total initial cost'
        aliases = ['gr_tot_init']
        dependencies = [
            GridSystemTotalInternalInitialCost,
            GridSystemTotalExternalInitialCost,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(GridSystemTotalInternalInitialCost) + \
                   self.get(GridSystemTotalExternalInitialCost)



.. _mvmax4-gridsystemtotalinternaldiscountedrecurringcost:

Grid system total internal discounted recurring cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > system total discounted recurring cost <mvmax4-gridsystemtotaldiscountedrecurringcost>`


::

    class GridSystemTotalInternalDiscountedRecurringCost(V):
    
        section = 'system (grid)'
        option = 'system total internal discounted recurring cost'
        aliases = ['gr_tot_idrc']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # Get
            childDataset = childVS.state[0]
            childNode = childVS.state[1]
            # If the system is grid and we are connecting a node that was not in the existing grid,
            if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
                # Get internal cost
                internalAnnualCost = childVS.get(costGrid.GridInternalSystemRecurringCostPerYear)
                dcff = self.get(finance.DiscountedCashFlowFactor)
                # Apply cost factor and add up internal cost
                self.value += (dcff * internalAnnualCost)



.. _mvmax4-gridsystemtotalinternalinitialcost:

Grid system total internal initial cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > system total initial cost <mvmax4-gridsystemtotalinitialcost>`


::

    class GridSystemTotalInternalInitialCost(V):
    
        section = 'system (grid)'
        option = 'system total internal initial cost'
        aliases = ['gr_tot_iic']
        default = 0
        units = 'dollars'
    
        def aggregate(self, childVS):
            # Get
            childDataset = childVS.state[0]
            childNode = childVS.state[1]
            # If the system is grid and we are connecting a node that was not in the existing grid,
            if childVS.get(System)[0] == 'g' and not childDataset.wasNodeAlreadyConnected(childNode):
                # Get internal cost
                internalCost = childVS.get(costGrid.GridInternalSystemInitialCost)
                # Add up internal cost
                self.value += internalCost



.. _mvmax4-gridsystemtotallevelizedcost:

Grid system total levelized cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > system total discounted demand <mvmax4-gridsystemtotaldiscounteddemand>`

- :ref:`system (grid) > system total discounted cost <mvmax4-gridsystemtotaldiscountedcost>`


::

    class GridSystemTotalLevelizedCost(V):
    
        section = 'system (grid)'
        option = 'system total levelized cost'
        aliases = ['gr_tot_lev']
        dependencies = [
            GridSystemTotalDiscountedDemand,
            GridSystemTotalDiscountedCost,
        ]
        units = 'dollars per kilowatt-hour'
    
        def compute(self):
            if self.get(GridSystemTotalDiscountedDemand) == 0:
                return 0
            return self.get(GridSystemTotalDiscountedCost) / float(self.get(GridSystemTotalDiscountedDemand))



.. _mvmax4-gridsystemtotalproposednetworklength:

Grid system total proposed network length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`metric > system <mvmax4-system>`


::

    class GridSystemTotalProposedNetworkLength(V):
    
        section = 'system (grid)'
        option = 'system total proposed network length'
        aliases = ['gr_tot_pnl']
        units = 'meters'
    
        # Don't understand why we need this
        dependencies = [System]
    
        def compute(self):
            return self.state[0].sumNetworkWeight(is_existing=False)



.. _mvmax4-costgrid-gridtransformeractualsystemcapacity:

Grid transformer actual system capacity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > available system capacities (transformer) <mvmax4-costgrid-gridtransformeravailablesystemcapacities>`

- :ref:`system (grid) > grid transformer actual system capacity counts <mvmax4-costgrid-gridtransformeractualsystemcapacitycounts>`

Derivatives

- :ref:`system (grid) > transformer cost <mvmax4-costgrid-gridtransformercost>`


::

    class GridTransformerActualSystemCapacity(V):
    
        section = 'system (grid)'
        option = 'grid transformer actual system capacity'
        aliases = ['gr_tr_acp']
        dependencies = [
            GridTransformerAvailableSystemCapacities,
            GridTransformerActualSystemCapacityCounts,
        ]
        units = 'kilowatts'
    
        def compute(self):
            return numpy.dot(
                self.get(GridTransformerAvailableSystemCapacities), 
                self.get(GridTransformerActualSystemCapacityCounts))



.. _mvmax4-costgrid-gridtransformeractualsystemcapacitycounts:

Grid transformer actual system capacity counts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > grid transformer desired system capacity <mvmax4-costgrid-gridtransformerdesiredsystemcapacity>`

- :ref:`system (grid) > available system capacities (transformer) <mvmax4-costgrid-gridtransformeravailablesystemcapacities>`

Derivatives

- :ref:`system (grid) > grid transformer actual system capacity <mvmax4-costgrid-gridtransformeractualsystemcapacity>`


::

    class GridTransformerActualSystemCapacityCounts(V):
    
        section = 'system (grid)'
        option = 'grid transformer actual system capacity counts'
        aliases = ['gr_tr_acps']
        c = dict(parse=store.unstringifyIntegerList, format=store.flattenList, validate='validateNumberList')
        dependencies = [
            GridTransformerDesiredSystemCapacity,
            GridTransformerAvailableSystemCapacities,
        ]
        units = 'capacity count list'
    
        def compute(self):
            return metric.computeSystemCounts(
                self.get(GridTransformerDesiredSystemCapacity), 
                self.get(GridTransformerAvailableSystemCapacities))



.. _mvmax4-costgrid-gridtransformeravailablesystemcapacities:

Grid transformer available system capacities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > grid transformer actual system capacity <mvmax4-costgrid-gridtransformeractualsystemcapacity>`

- :ref:`system (grid) > grid transformer actual system capacity counts <mvmax4-costgrid-gridtransformeractualsystemcapacitycounts>`


::

    class GridTransformerAvailableSystemCapacities(V):
    
        section = 'system (grid)'
        option = 'available system capacities (transformer)'
        aliases = ['gr_tr_cps']
        c = dict(parse=store.unstringifyDescendingFloatList, format=store.flattenList, validate='validateNumberList')
        default = '1000 900 800 700 600 500 400 300 200 100 90 80 70 60 50 40 30 20 15 5'
        units = 'kilowatts list'



.. _mvmax4-costgrid-gridtransformercost:

Grid transformer cost
^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > transformer cost per grid system kilowatt <mvmax4-costgrid-gridtransformercostpergridsystemkilowatt>`

- :ref:`system (grid) > grid transformer actual system capacity <mvmax4-costgrid-gridtransformeractualsystemcapacity>`

Derivatives

- :ref:`system (grid) > internal system initial cost <mvmax4-costgrid-gridinternalsysteminitialcost>`

- :ref:`system (grid) > transformer operations and maintenance cost per year <mvmax4-costgrid-gridtransformeroperationsandmaintenancecostperyear>`

- :ref:`system (grid) > transformer replacement cost per year <mvmax4-costgrid-gridtransformerreplacementcostperyear>`


::

    class GridTransformerCost(V):
    
        section = 'system (grid)'
        option = 'transformer cost'
        aliases = ['gr_tr']
        dependencies = [
            GridTransformerCostPerGridSystemKilowatt,
            GridTransformerActualSystemCapacity,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(GridTransformerCostPerGridSystemKilowatt) * self.get(GridTransformerActualSystemCapacity)



.. _mvmax4-costgrid-gridtransformercostpergridsystemkilowatt:

Grid transformer cost per grid system kilowatt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > transformer cost <mvmax4-costgrid-gridtransformercost>`


::

    class GridTransformerCostPerGridSystemKilowatt(V):
    
        section = 'system (grid)'
        option = 'transformer cost per grid system kilowatt'
        aliases = ['gr_tr_ckw']
        default = 1000
        units = 'dollars per kilowatt'



.. _mvmax4-costgrid-gridtransformerdesiredsystemcapacity:

Grid transformer desired system capacity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`demand (peak) > projected peak nodal demand <mvmax4-demand-projectedpeaknodaldemand>`

- :ref:`system (grid) > distribution loss <mvmax4-costgrid-distributionloss>`

Derivatives

- :ref:`system (grid) > grid transformer actual system capacity counts <mvmax4-costgrid-gridtransformeractualsystemcapacitycounts>`


::

    class GridTransformerDesiredSystemCapacity(V):
    
        section = 'system (grid)'
        option = 'grid transformer desired system capacity'
        aliases = ['gr_tr_dcp']
        dependencies = [
            demand.ProjectedPeakNodalDemand,
            DistributionLoss,
        ]
        units = 'kilowatts'
    
        def compute(self):
            return self.get(demand.ProjectedPeakNodalDemand) / float(1 - self.get(DistributionLoss))



.. _mvmax4-costgrid-gridtransformerlifetime:

Grid transformer lifetime
^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > transformer replacement cost per year <mvmax4-costgrid-gridtransformerreplacementcostperyear>`


::

    class GridTransformerLifetime(V):
    
        section = 'system (grid)'
        option = 'transformer lifetime'
        aliases = ['gr_tr_life']
        c = dict(check=store.assertPositive)
        default = 10
        units = 'years'



.. _mvmax4-costgrid-gridtransformeroperationsandmaintenancecostperyear:

Grid transformer operations and maintenance cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > transformer operations and maintenance cost per year as fraction of transformer cost <mvmax4-costgrid-gridtransformeroperationsandmaintenancecostperyearasfractionoftransformercost>`

- :ref:`system (grid) > transformer cost <mvmax4-costgrid-gridtransformercost>`

Derivatives

- :ref:`system (grid) > internal system recurring cost per year <mvmax4-costgrid-gridinternalsystemrecurringcostperyear>`


::

    class GridTransformerOperationsAndMaintenanceCostPerYear(V):
    
        section = 'system (grid)'
        option = 'transformer operations and maintenance cost per year'
        aliases = ['gr_tr_om']
        dependencies = [
            GridTransformerOperationsAndMaintenanceCostPerYearAsFractionOfTransformerCost,
            GridTransformerCost,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(GridTransformerOperationsAndMaintenanceCostPerYearAsFractionOfTransformerCost) * self.get(GridTransformerCost)



.. _mvmax4-costgrid-gridtransformeroperationsandmaintenancecostperyearasfractionoftransformercost:

Grid transformer operations and maintenance cost per year as fraction of transformer cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Derivatives

- :ref:`system (grid) > transformer operations and maintenance cost per year <mvmax4-costgrid-gridtransformeroperationsandmaintenancecostperyear>`


::

    class GridTransformerOperationsAndMaintenanceCostPerYearAsFractionOfTransformerCost(V):
    
        section = 'system (grid)'
        option = 'transformer operations and maintenance cost per year as fraction of transformer cost'
        aliases = ['gr_tr_omf']
        default = 0.03



.. _mvmax4-costgrid-gridtransformerreplacementcostperyear:

Grid transformer replacement cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`system (grid) > transformer cost <mvmax4-costgrid-gridtransformercost>`

- :ref:`system (grid) > transformer lifetime <mvmax4-costgrid-gridtransformerlifetime>`

Derivatives

- :ref:`system (grid) > internal system recurring cost per year <mvmax4-costgrid-gridinternalsystemrecurringcostperyear>`


::

    class GridTransformerReplacementCostPerYear(V):
    
        section = 'system (grid)'
        option = 'transformer replacement cost per year'
        aliases = ['gr_tr_rep']
        dependencies = [
            GridTransformerCost,
            GridTransformerLifetime,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(GridTransformerCost) / float(self.get(GridTransformerLifetime))



.. _mvmax4-costgrid-lowvoltagelineequipmentcost:

Low voltage line equipment cost
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`distribution > low voltage line equipment cost per connection <mvmax4-costdistribution-lowvoltagelineequipmentcostperconnection>`

- :ref:`system (grid) > internal connection count <mvmax4-costgrid-gridinternalconnectioncount>`

Derivatives

- :ref:`system (grid) > internal system initial cost <mvmax4-costgrid-gridinternalsysteminitialcost>`

- :ref:`system (grid) > low voltage line equipment operations and maintenance cost per year <mvmax4-costgrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear>`


::

    class LowVoltageLineEquipmentCost(V):
    
        section = 'system (grid)'
        option = 'low voltage line equipment cost'
        aliases = ['gr_le']
        dependencies = [
            costDistribution.LowVoltageLineEquipmentCostPerConnection,
            GridInternalConnectionCount,
        ]
        units = 'dollars'
    
        def compute(self):
            return self.get(costDistribution.LowVoltageLineEquipmentCostPerConnection) * self.get(GridInternalConnectionCount)



.. _mvmax4-costgrid-lowvoltagelineequipmentoperationsandmaintenancecostperyear:

Low voltage line equipment operations and maintenance cost per year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dependencies

- :ref:`distribution > low voltage line equipment operations and maintenance cost as fraction of equipment cost <mvmax4-costdistribution-lowvoltagelineequipmentoperationsandmaintenancecostperyearasfractionofequipmentcost>`

- :ref:`system (grid) > low voltage line equipment cost <mvmax4-costgrid-lowvoltagelineequipmentcost>`

Derivatives

- :ref:`system (grid) > internal system recurring cost per year <mvmax4-costgrid-gridinternalsystemrecurringcostperyear>`


::

    class LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYear(V):
    
        section = 'system (grid)'
        option = 'low voltage line equipment operations and maintenance cost per year'
        aliases = ['gr_le_om']
        dependencies = [
            costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost,
            LowVoltageLineEquipmentCost,
        ]
        units = 'dollars per year'
    
        def compute(self):
            return self.get(costDistribution.LowVoltageLineEquipmentOperationsAndMaintenanceCostPerYearAsFractionOfEquipmentCost) * self.get(LowVoltageLineEquipmentCost)



Metric
------

.. _mvmax4-metric:

Metric
^^^^^^

Dependencies

- :ref:`system (off-grid) > system nodal discounted cost <mvmax4-costoffgrid-offgridsystemnodaldiscountedcost>`

- :ref:`system (off-grid) > system nodal levelized cost <mvmax4-costoffgrid-offgridsystemnodallevelizedcost>`

- :ref:`system (mini-grid) > system nodal discounted cost <mvmax4-costminigrid-minigridsystemnodaldiscountedcost>`

- :ref:`system (mini-grid) > system nodal levelized cost <mvmax4-costminigrid-minigridsystemnodallevelizedcost>`

- :ref:`system (grid) > internal system nodal discounted cost <mvmax4-costgrid-gridinternalsystemnodaldiscountedcost>`

- :ref:`system (grid) > internal system nodal levelized cost <mvmax4-costgrid-gridinternalsystemnodallevelizedcost>`

- :ref:`system (grid) > external nodal discounted cost per meter <mvmax4-costgrid-gridexternalsystemnodaldiscountedcostpermeter>`


::

    class Metric(V):
        'Maximum length of medium voltage line for which grid extension is cheaper than standalone options'
    
        section = 'metric'
        option = 'maximum length of medium voltage line extension'
        aliases = ['mvmax']
        dependencies = [
            costOffGrid.OffGridSystemNodalDiscountedCost,
            costOffGrid.OffGridSystemNodalLevelizedCost,
            costMiniGrid.MiniGridSystemNodalDiscountedCost,
            costMiniGrid.MiniGridSystemNodalLevelizedCost,
            costGrid.GridInternalSystemNodalDiscountedCost,
            costGrid.GridInternalSystemNodalLevelizedCost,
            costGrid.GridExternalSystemNodalDiscountedCostPerMeter,
        ]
        units = 'meters'
    
        def compute(self):
            # Compute levelized costs
            self.get(costOffGrid.OffGridSystemNodalLevelizedCost)
            self.get(costMiniGrid.MiniGridSystemNodalLevelizedCost)
            self.get(costGrid.GridInternalSystemNodalLevelizedCost)
            # Compute the cost of the cheapest standalone option for the node
            standaloneCost = min(
                self.get(costOffGrid.OffGridSystemNodalDiscountedCost),
                self.get(costMiniGrid.MiniGridSystemNodalDiscountedCost))
            # Compute the (non-negative) amount of money we have left to spend on grid extension
            gridExternalBudget = max(0, standaloneCost - self.get(costGrid.GridInternalSystemNodalDiscountedCost))
            # Compute the length of line we are allowed for grid extension
            return gridExternalBudget / float(self.get(costGrid.GridExternalSystemNodalDiscountedCostPerMeter))



.. _mvmax4-system:

System
^^^^^^

Dependencies

- :ref:`demand > projected nodal demand per year <mvmax4-demand-projectednodaldemandperyear>`

- :ref:`system (mini-grid) > system nodal discounted cost <mvmax4-costminigrid-minigridsystemnodaldiscountedcost>`

- :ref:`system (off-grid) > system nodal discounted cost <mvmax4-costoffgrid-offgridsystemnodaldiscountedcost>`

Derivatives

- :ref:`system (grid) > system total existing network length <mvmax4-gridsystemtotalexistingnetworklength>`

- :ref:`system (grid) > system total proposed network length <mvmax4-gridsystemtotalproposednetworklength>`


::

    class System(V):
    
        section = 'metric'
        option = 'system'
        aliases = ['system']
        c = dict(parse=str)
        dependencies = [
            demand.ProjectedNodalDemandPerYear,
            costMiniGrid.MiniGridSystemNodalDiscountedCost,
            costOffGrid.OffGridSystemNodalDiscountedCost,
        ]
    
        def compute(self):
            # If the demand is positive,
            if self.get(demand.ProjectedNodalDemandPerYear) == 0:
                return 'unelectrified'
            # If grid is chosen,
            elif self.state[0].isNodeConnected(self.state[1]):
                return 'grid'
            # If mini-grid is chosen,
            elif self.get(costMiniGrid.MiniGridSystemNodalDiscountedCost) < self.get(costOffGrid.OffGridSystemNodalDiscountedCost):
                return 'mini-grid'
            # If off-grid is chosen,
            else:
                return 'off-grid'


