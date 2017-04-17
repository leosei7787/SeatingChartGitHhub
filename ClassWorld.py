#!/usr/bin/python3.6
import copy
from random import randint

import Utils
from ClassPerson import Person
from ClassTable import Table
from ClassPlan import Plan


######### CLASS FOR THE WORLD ########
class World(object):
  'world of plan population'
  guests = []
  plans = []
  table_configuration = []
  weight_config = {}
  total_tables = 0
  verbose = False

  def __init__(self,guests,table_configuration,weight_config,verbose):
    self.guests = guests
    self.table_configuration = table_configuration
    self.weight_config = weight_config
    for table in table_configuration:
      self.total_tables += table[0]
    self.verbose = verbose
    if self.verbose == True:
      print("%d total tables per plan"%self.total_tables)
    self.sortGuests()
    
  def seedRandomPlans(self,number):
    for i in list(range(number)):
      plan = self.newRandomPlan(i)
      self.plans.append(plan)
      if self.verbose == True:
        print("new random plan %s"%plan.name)

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

  def sortPlans(self):    
    if len(self.plans) == 0:
      return
    self.plans  = sorted(self.plans, key=lambda obj: obj.getScore())

  def newRandomPlan(self,i):
    name = "%s"%i
    plan = Plan(name,self.total_tables,[])
    id_count = 0
    total_seats = 0
    # Go through configuration of table
    for table_type in self.table_configuration:
      quantity = table_type[0]
      seats = table_type[1]
      for i in list(range( quantity ) ):
        # add table to plan
        plan.addTable( Table(id_count,seats,self.weight_config) )
        total_seats += seats
        id_count += 1
    print("%d table created %d total seats"%(id_count,total_seats))

    # Validate there is enough seats for all guests
    total_guests = self.getTotalGuests()

    if total_seats < total_guests:
      print('not enough room for %d guests (%d seats)'%(total_guests,total_seats))
      return

    Utils.setUsersOnTable(self.guests,plan.tables,False)
    return plan

  def iterate(self,round):
    for i in list(range(round)):
      print("\n<<<<<< round %d >>>>>>>>>>"%i)
      if self.verbose == True:
        print(self.toStringlist())

      self.updateGeneration()
      best_plan = self.getBestplan() 
      print("New best plan %s, score %d"%(best_plan.name,best_plan.getScore()))

  def updateGeneration(self):
    # go through plans
    for parent_plan in self.plans:
      best_plan = parent_plan
      best_score = parent_plan.getScore()

      # Compute number of children from score (higher score = more children)
      number_children = 1
      if best_score > 10:
        number_children = randint(1, int(best_score/10))

      if self.verbose == True:
        print("plan %s (%d) up for reproduction with %d children"%(parent_plan.name,parent_plan.getScore(), number_children))
        print(parent_plan.toStringList())
 
      children = []
      for child in list(range(number_children)):
        # Create new child as duplicate of paren (with name change)
        child_name = "%s-%d"%(parent_plan.name,child)
        temp_tables = []
        for table in  parent_plan.tables:
          temp_tables.append(table)
        child_plan = Plan(child_name,self.total_tables,temp_tables)    
        children.append(child_plan)

        if self.verbose == True:
          print("Children %s (%d) created"%(child_plan.name,child_plan.getScore()))

      # Go over each child to muate them and check if better than parent.
      to_swap = False
      for child_plan in children:
        if self.verbose == True:
          print("child %s (%d) up for mutation"%(child_plan.name,child_plan.getScore()))
        child_plan.mutate(self.verbose)
        child_score = child_plan.getScore()

        if self.verbose == True:
          print("child %s (%d) done with mutations"%(child_plan.name,child_plan.getScore()))
        if child_score > best_score:
          best_plan = child_plan
          best_score = child_score
          to_swap = True
      
      if to_swap == True:
        self.swapPlans(parent_plan,best_plan)

  def swapPlans(self,old,new):
    if self.verbose == True:
      print (self.toStringlist())
    
    temp_plans = []
    for plan in self.plans:
      if plan.name == old.name:
        temp_plans.append(new)
      else:
        temp_plans.append(plan)
    self.plans = temp_plans

    if self.verbose == True:
      print ("Swapped %s for %s"%(old.toString(),new.toString()))
      print (self.toStringlist())

  def getBestplan(self):
    self.sortPlans()
    return self.plans[ (len(self.plans)-1) ]

  def getTotalGuests(self):
    total = 0
    for guest in self.guests:
      total += guest.seats
    return total

  def toStringDebug(self):
    temp = " --- total world update -- "
    for plan in self.plans:
      temp += plan.toStringDebug()
    return temp

  def toStringlist(self):
    temp = " --- total world update -- \n"
    for plan in self.plans:
      temp += "\n plan %s Score:%d"%(plan.name,plan.getScore())
    return temp


