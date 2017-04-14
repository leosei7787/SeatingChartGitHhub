#!/usr/bin/python3.6
from random import randint
import copy
import Utils


###### CLASS PLAN DE TABLE ######
class Plan:
  'Define a TablePlan'

  def __init__(self,name, tables = []):
    self.name = name
    self.tables = tables

  def addTable(self, table):
    self.tables.append(table)
    self.sortTable()

  def setTables(self,tables):
    self.tables = tables
    self.sortTable()

  def removeTable(self,table):
    temp_tables = []
    for t in self.tables:
      if t.id != table.id:
        temp_tables.append(t)
    self.tables = temp_tables

  def getScore(self):
    if len(self.tables) == 0:
      return 0

    self.sortTable()
    score_list = []
    for table in self.tables:
      score_list += [table.getScore()]
    
    # Compute plan score
    return sum(score_list)/float(len(score_list)) #self.tables[0].getScore() 

  def sortTable(self):
    self.tables = sorted(self.tables, key=lambda obj: obj.getScore())

  def getTotalSeats(self):
    total = 0
    for table in self.tables:
      total += table.seats
    return total

  def toString(self):
    return "%s, score %d"%(self.name,self.getScore())
  
  def toStringList(self):
    temp_tables = []
    temp = "--> PLAN: %s (%d):"%(self.name,self.getScore())
    for table in self.tables:
      temp_tables.append(table.toStringList())
    temp += "\n".join(temp_tables)
    return temp  


  def toStringDebug(self):
    temp = "--> PLAN: %s (%d):"%(self.name,self.getScore())
    for table in self.tables:
      temp += "\n-%s\n"%table.toStringDebug()
    return temp    

  def getTotalTables(self):
    return len(self.tables)


  def mutate(self,verbose = False):
    
    #take worse table and swap with random other
    self.sortTable()
    table1_index = 0
    table2_index = randint(1,len(self.tables)-1)

    # create new temporary table instances, copies of initial tables
    table1 = copy.deepcopy(self.tables[table1_index])
    table2 = copy.deepcopy(self.tables[table2_index])
    
    # Create list of combined persons at tables to swap
    combined_persons = table1.persons[:] + table2.persons[:]

    # Remove existing guest from temp tables instances
    table1.emptyTable()
    table2.emptyTable()

    if verbose == True:
      print("\n====  before mutation === ")
      print(table1.toStringList())
      print(table2.toStringList())
      print("\n")

    # randomly assign set of persones on two temporary tables
    Utils.setUsersOnTable(combined_persons,[table1,table2],verbose)

    # update plan tables
    self.tables[table1_index] = table1
    self.tables[table2_index] = table2
    
    if verbose == True:
      print("\n====  After mutation === ")
      for table in new_tables:
        print(table.toStringList())
      print("\n")