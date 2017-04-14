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

weight_config = {"group":10,"language":1,"age":5,"nogo_list":[]}

# Max child and max permutations
mutation_config = {"max_childs":1}

verbose = False
seeds = 2
Nb_generations = 3

# get file
file = sys.argv[1]
nogo = sys.argv[2]
# ---------------------------------------------


# get guests
guests = CSVImport.getGuests(file,header,1000)
#update nogo
weight_config["nogo_list"] = Utils.getNogo(nogo)
# Start world
world = World(guests,table_configuration,weight_config,mutation_config)
# Seeds (number of seeds)
world.seedRandomPlans(seeds,verbose)
# Iterate (round, verbose)
world.iterate(Nb_generations,verbose)

# Output best plan
best_plan = world.getBestplan()
print("---\n\n")
print(best_plan.toStringDebug())
  
  