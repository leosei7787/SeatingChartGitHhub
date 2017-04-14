#!/usr/bin/python3.6
import copy
from random import randint

from ClassPerson import Person
from ClassTable import Table
from ClassPlan import Plan

######### CLASS FOR THE WORLD ########
class World:
  'world of plan population'
  guests = []
  plans = []
  table_configuration = []
  weight_config = {}
  mutation_config = {}

  def __init__(self,guests,table_configuration,weight_config,mutation_config):
    self.guests = guests
    self.table_configuration = table_configuration
    self.weight_config = weight_config
    self.mutation_config = mutation_config

  def seedRandomPlans(self,number):
    for i in list(range(number)):
      self.newRandomPlan(i)

  def addPlan(self,plan):
    self.plans.append(plan)

  def removePlan(self,plan):
    temp_plans = []
    for p in self.plans:
      if p.name != plan.name:
        temp_plans.append(p)
    self.plans = temp_plans
  
  def sortGuests(self):
    self.guests = sorted(self.guests, key=lambda obj: obj.seats,reverse=True)

  def getGuestsList(self):
    temp =""
    for guest in self.guests:
      temp += "%s (%d) "%(guest.name,guest.seats)
    return temp

  def newRandomPlan(self,i):
    name = "plan %s"%i
    plan = Plan(name)
    id_count = 0
    total_seats = 0
    # Go through configuration of table
    for config in self.table_configuration:
      number = config[0]
      seats = config[1]
      for i in list(range( number ) ):
        # add table to plan
        plan.addTable( Table(id_count,seats,self.weight_config) )
        total_seats += seats
        id_count += 1

    # Validate there is enough seats for all guests
    total_guests = self.getTotalGuests()
    print('%d guests: %d seats)'%(total_guests,total_seats))
    if total_seats < total_guests:
      print('not enough room for %d guests (%d seats)'%(total_guests,total_seats))
      return

    plan.setUsersOnTable(self.guests,plan.tables,False)
    self.plans.append(plan)

  def iterate(self,round):
    for i in list(range(round)):
      print("\n<<<<<< round %d >>>>>>>>>>"%i)
      #print(self.getPlansList())
      self.updateGeneration()
      print("\nbest plan score now %.4f"%self.getBestplan().score)
      #print(self.getBestplan().toStringDebug())

  def updateGeneration(self):
    max_permutations = self.mutation_config["max_permutations"]
    max_childs = self.mutation_config["max_childs"]
    

    # go through plans
    for parent_plan in self.plans:
      best_plan = parent_plan
      best_score = parent_plan.score
      

      # Define max nb of mutation, highest score would get less permutations
      plan_max_permutations = 1 + int(max_permutations * (1 - parent_plan.score) )
      # define number of children, highest score would get more children
      temp_childs = 10#1 + int(float(parent_plan.score) * int(max_childs))
 
      to_swap = False
      for child in list(range(temp_childs)):
        #print("new child")
        #create new child
        temp_permutations = randint(1, plan_max_permutations)
        child_name = "%s-%d"%(parent_plan.name,child)
        child_tables = parent_plan.tables
        child_plan = Plan(child_name)
        child_plan.setTables(child_tables)

        # Mutate child
        child_plan.mutate(temp_permutations)
        child_score = child_plan.score
        #print("child instance %d with %d permutations"%(child,temp_permutations))
        if child_score > best_score:
          best_plan = child_plan
          best_score = child_score
          to_swap = True
      
      if to_swap == True:
        self.swapPlans(parent_plan,best_plan)
      print(self.getPlansList())
      #self.debugPlans()

  def swapPlans(self,old,new):
    self.removePlan(old)
    self.addPlan(new)
    #print ("sawping plan %s (%.4f) for plan %s (%.4f)"%(old.name,old.score,new.name,new.score))

    

  def debugPlans(self):
    print("----Current population update----")
    for plan in self.plans:
      print(plan.toString())
    print("---------------------------------")

  def getPlansList(self):
    temp = "POPULATION: "
    for plan in self.plans:
      temp += "%s (%.4f), "%(plan.name,plan.score)
    return temp

  def getBestplan(self):
    best_plan = self.plans[0]
    best_score = best_plan.score
   
    for plan in self.plans[1:]:
      plan_score = plan.score
      if plan_score > best_score:
        best_score = plan_score
        best_plan = plan
    return best_plan

  def getTotalGuests(self):
    total = 0
    for guest in self.guests:
      total += guest.seats
    return total