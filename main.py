#!/usr/bin/python3.6
import sys

# Custom packages
import CSVImport
import Utils
from ClassWorld import World

#----------configurations ----------------
header = {"name":0,"groups":1,"seats":2,"age":3,"language":4}
# Table configuration, [Nb table,Nb seats / table]

table_configuration = [[12,8],[3,10]]
#table_configuration = [[3,4],[1,6]]

#Score weighting

# Age score: -1 per (age diff) / (age weight)
weight_config = {"group":10,"language":1,"age":5, "nogo":50,
                "nogo_list":[]}

# Max child for best plans
mutation_config = {"max_childs":1,"max_permutations":3}

# get file
file = sys.argv[1]
# ---------------------------------------------

# get guests
guests = CSVImport.getGuests(file,header,100)

# Start world
world = World(guests,table_configuration,weight_config,mutation_config)

#Seeds (number of seeds)
world.seedRandomPlans(5)
#Iterate (round, verbose)
world.iterate(150,False)


best_plan = world.getBestplan()
print("---\n\n")
print(best_plan.toStringDebug())

  
  