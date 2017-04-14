#!/usr/bin/python3.6
from random import randint
import Utils


###### CLASS PLAN DE TABLE ######
class Plan:
  'Define a TablePlan'

  def __init__(self,name):
    self.tables = []
    self.score = 1
    self.name = name

  def addTable(self, table):
    self.tables.append(table)
    self.sortTable()
    self.updateScore()

  def setTables(self,tables):
    self.tables = tables
    self.sortTable()
    self.updateScore()

  def removeTable(self,table):
    temp_tables = []
    for t in self.tables:
      if t.id != table.id:
        temp_tables.append(t)
    self.tables = temp_tables

  def updateScore(self):
    self.sortTable()
    # Get min score of tables

    score_list = []
    for table in self.tables:
      score_list += [table.score]
    self.score = sum(score_list)#/float(len(score_list))
    #print ("table score, total score %d "%self.score)
    #print (score_list)
    return self.score

  def sortTable(self):
    for table in self.tables:
      table.updateScore()
    self.tables = sorted(self.tables, key=lambda obj: obj.score)

  def getTotalSeats(self):
    total = 0
    for table in self.tables:
      total += table.seats
    return total

  def toString(self):
    temp = "PLAN: %s (%.4f)"%(self.name,self.score)
    for table in self.tables:
      temp += "\n-%s"%table.toString()
    return temp

  def toStringDebug(self):
    temp = "--> PLAN: %s (%d):"%(self.name,self.score)
    for table in self.tables:
      temp += "\n-%s\n"%table.toStringDebug()
    return temp    

  def getTotalTables(self):
    return len(self.tables)


  def mutate(self,temp_permutations):
    for i in list(range(temp_permutations)):
      self.sortTable()

      #take worse table with random table for swap
      table1_index = 0
      table2_index = randint(1,len(self.tables)-1)
      table1 = self.tables[table1_index]
      table2 = self.tables[table2_index]

      persons = table1.persons + table2.persons
      table1.persons = []
      table2.persons = []
      tables = [table1,table2]
      Utils.setUsersOnTable(persons,tables,False)
    self.updateScore()

