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


  def mutate(self,temp_permutations,verbose = False):
    for i in list(range(temp_permutations)):
      self.sortTable()

      #take worse table with random table for swap
      table1_index = 0
      table2_index = randint(1,len(self.tables)-1)

      table1 = copy.deepcopy(self.tables[table1_index])
      table2 = copy.deepcopy(self.tables[table2_index])
      
      # Store persons from two tables to swap.
      combined_persons = table1.persons[:] + table2.persons[:]

      table1.emptyTable()
      table2.emptyTable()
      new_tables = [table1,table2]

      if verbose == True:
        print("\n====  before mutation === ")
        for table in new_tables:
          print(table.toStringList())
        print("\n")

      # randomly assign set of persones on set of tables
      Utils.setUsersOnTable(combined_persons,new_tables,verbose)

      #update tables
      self.tables[table1_index] = table1
      self.tables[table2_index] = table2
      
      if verbose == True:
        print("\n====  After mutation === ")
        for table in new_tables:
          print(table.toStringList())
        print("\n")