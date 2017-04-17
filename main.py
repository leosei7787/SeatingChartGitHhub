#!/usr/bin/python3.6
import copy
import sys
import pickle

# Custom packages
import CSVImport
import Utils
from ClassWorld import World

#----------configurations ----------------
header = {"name":0,"groups":1,"seats":2,"age":3,"language":4}

# Table configuration, [Nb table,Nb seats / table]
table_configuration = [[11,8],[3,10]]
total_tables = 15

# Max age diff kicks score to zero when not in same group. 
# Nogo list will kick table score to zero
weight_config = {"group":20,"language":1,"age":1,"max_age_diff":20,"nogo_list":[]}

verbose = False
seeds = 10
Nb_generations = 300

best_plan_file = "best_plan.pickle"
start_from_previous_best_plan = True
# --------------------------------------------



# get guest and nogo files from args
file = sys.argv[1]
nogo = sys.argv[2]

# get guests from file, with header and max rows
guests = CSVImport.getGuests(file,header,1000)
#update nogo
weight_config["nogo_list"] = Utils.getNogo(nogo)
# Start world
world = World(guests,table_configuration,weight_config,verbose)

# load best previous plan
if start_from_previous_best_plan == True:
  with open(best_plan_file, 'rb') as f:
    best_plan = pickle.load(f)
  for i in list(range(seeds)):
    temp_best_plan = copy.deepcopy(best_plan)
    temp_best_plan.name = "%d"%(i)
    world.addPlan(temp_best_plan)
  # adding one random to keep exploring.
  world.seedRandomPlans(1)
else:
  # Seeds (number of seeds)
  world.seedRandomPlans(seeds)

# Iterate (round, verbose)
world.iterate(Nb_generations)


# Output best plan
best_plan = world.getBestplan()
print("---\n\n")
print(best_plan.toStringDebug())

with open(best_plan_file, 'wb') as f:
    pickle.dump(best_plan, f, pickle.HIGHEST_PROTOCOL)

