#!/usr/bin/python3.6
import sys

# Custom packages
import CSVImport
from ClassWorld import World

#----------configurations ----------------
header = {"name":0,"groups":1,"seats":2,"age":3,"language":4}
# Table configuration, [Nb table,Nb seats / table]
table_configuration = [[13,8],[3,10]]
#table_configuration = [[4,30],[1,32]]

#Score weighting
weight_config = {"group":0.3,"language":0.3,"age":0.3,"seat":0.1}

# Max child for best plans
mutation_config = {"max_childs":20,"max_permutations":100}

# get file
file = sys.argv[1]
# ---------------------------------------------

guests = CSVImport.getGuests(file,header,200)

# Start word
world = World(guests,table_configuration,weight_config,mutation_config)
# Sort guess from most seats taken to less to make table fitting easier.
world.sortGuests()

#Seeds (number of seeds)
world.seedRandomPlans(2)
#Iterate (round)
world.iterate(5)


best_plan = world.getBestplan()
print("---\n\n")
print(best_plan.toStringDebug())


  
  