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
weight_config = {"group":5,"language":1,"age":5, "nogo":50,
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
world.seedRandomPlans(3)
#Iterate (round, verbose)
world.iterate(20,False)


best_plan = world.getBestplan()
print("---\n\n")
print(best_plan.toStringDebug())

  
  




# TEST SECTION
"""
Jack = Person("Jack test",2,["A","B"],["EN","FR"],30)
Tom = Person("Tom Foo",1,["A","C"],["EN","HE"],35)
Foo = Person("Foo Ab",2,["D"],["EN","HE"],25)
Bar = Person("Bar BC",2,["C","D"],["FR"],30)


table1 = Table(1,8)
table1.setPersons([Jack,Tom,Foo,Bar])

print (table1.toString())
print ("Score languages %.2f, Score Groups %.2f, Score Age %.2f"% (table1.getScoreLanguage(), table1.getScoreGroup(), table1.getScoreAge()))
print ("Score total %.2f"%(table1.getScore()))
"""

     