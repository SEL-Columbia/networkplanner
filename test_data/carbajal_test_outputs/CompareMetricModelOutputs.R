##Testing MVMax4 to MVMax5
##
rm(list=ls())
require(plyr)


#import test files developed by CN command line prompts
setwd("~/github/local/networkplanner/")
mv4 <- read.csv("MV4sample_demand_output_updated1216V2.csv") 
mv5 <- read.csv("MV5sample_demand_output_updated1216V2.csv")

#also import indexes for each metric model for better subsetting
mv4_index <- read.csv("mapping_mvmax4.csv")
mv5_index <- read.csv("mapping_mvmax5.csv")

#Identify parameters associated with MiniGrids
MG_Params_mv4 <- subset(mv4_index, (section == "system (mini-grid)" |
                                      alias == "p_pkdem" |
                                      alias == "p_dem"
                                    ))                                

MG_Subset_mv4 <- mv4[, which(names(mv4) %in% MG_Params_mv4$alias)]

#Identify parameters associated with MiniGrids
MG_Params_mv5 <- subset(mv5_index, (section == "system (mini-grid)" |
                                      alias == "p_pkdem" |
                                      alias == "p_dem"))
MG_Subset_mv5 <- mv5[, which(names(mv5) %in% MG_Params_mv5$alias)]

##Change names so i can interpret them for 4
#ensure dataframes are in similar order
MG_Subset_mv4 <- MG_Subset_mv4[,order(names(MG_Subset_mv4))]
new_names4 <- MG_Params_mv4[,c("alias", "class")]
new_names4 <- new_names4[order(new_names4$alias),]
#assign the corresponding class name to replace the alias
names(MG_Subset_mv4) = new_names4$class

##Change names so i can interpret them for 5
#ensure dataframes are in similar order
MG_Subset_mv5 <- MG_Subset_mv5[,order(names(MG_Subset_mv5))]
new_names5 <- MG_Params_mv5[,c("alias", "class")]
new_names5 <- new_names5[order(new_names5$alias),]
#assign the corresponding class name to replace the alias
names(MG_Subset_mv5) = new_names5$class


