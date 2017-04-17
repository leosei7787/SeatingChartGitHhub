#!/usr/bin/python3.6
from random import randint
import copy
import Utils

###### CLASS PLAN DE TABLE ######
class Plan(object):
  'Define a TablePlan'

  def __init__(self,name,total_tables, tables = []):
    self.name = name
    self.tables = tables
    self.total_tables =  total_tables

  def addTable(self, table):
    if len(self.tables) == self.total_tables:
      print("No room for tables %s"%table.id)
      print(self.toStringList())

    self.tables.append(table)
    self.sortTable()

  def setTables(self,tables):
    if len(tables) > self.total_tables:
      print("too many tables to add")
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
      table_score = table.getScore()
      score_list += [table_score]
 
    # Compute plan score as avg counting worse table 
    score = sum(score_list)/float(len(score_list)) + self.tables[0].getScore()  
    return score

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
    temp = "--> PLAN: %s (%d):\n"%(self.name,self.getScore())
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

    if verbose == True:
      print("\n====  before mutation === ")
      print(table1.toStringList())
      print(table2.toStringList())
      print("\n")

    # Remove existing guest from temp tables instances
    table1.emptyTable()
    table2.emptyTable()

    # randomly assign set of persones on two temporary tables
    Utils.setUsersOnTable(combined_persons,[table1,table2],verbose)

    # update plan tables
    self.tables[table1_index] = table1
    self.tables[table2_index] = table2
    
    if verbose == True:
      print("\n====  After mutation === ")
      print(table1.toStringList())
      print(table2.toStringList())
      print("\n")