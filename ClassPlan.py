#!/usr/bin/python3.6
from random import randint


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

  def updateScore(self):
    # Get min score of tables
    self.sortTable()
    self.score = self.tables[0].score

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
    temp = "PLAN: %s (%.4f):"%(self.name,self.score)
    for table in self.tables:
      temp += "\n-%s\n"%table.toStringDebug()
    return temp    

  def getList(self):
    temp = ""
    for table in self.tables:
      temp += "table %d (%.4f)"%(table.id,table.score)
    return temp

  def getTables(self):
    return self.tables

  def getTotalTables(self):
    return len(self.tables)

  def getWorseTable(self):
    worse_table = self.tables[0]
    for table in self.tables[1:]:
      if table.score<worse_table.score:
        worse_table = table
    return worse_table

  def setUsersOnTable(self,persons,tables,debug):
    persons = sorted(persons, key=lambda obj: obj.seats,reverse=True)
    # randomly add guests to table
    total_table = len(tables)
    for person in persons:
      # pick a random table
      selected_table = randint(0,total_table-1)
      table = tables[selected_table]
      # add to table
      added = table.addPerson(person,debug)
      if added != True:
        tried = selected_table
        selected_table = (selected_table + 1) % total_table
        while tried != selected_table and added != True:
         table = tables[selected_table]
         added = table.addPerson(person,debug)
         selected_table = (selected_table + 1) % total_table

    self.updateScore()

  def mutate(self,temp_permutations):
    for i in list(range(temp_permutations)):
      #print("new permutation")

      #random table for swap
      table1_index = randint(0,len(self.tables)-1)
      table2_index = (table1_index + 1) % len(self.tables)
      table1 = self.tables [table1_index]
      table2 = self.tables [table2_index]

      persons = table1.persons + table2.persons
      table1.persons = []
      table2.persons = []
      tables = [table1,table2]
      self.setUsersOnTable(persons,tables,False)
      

      '''
      if len(table1.persons) == 0:
        #print("there is no one at table %s"%table1.id)
        #print(table1.toString())
        continue
      else:
        person1 = table1.persons[randint(0,len(table1.persons)-1)]
      seats1 = person1.seats

      index_table_2 = randint(0,len(self.tables)-1)
      table2 = self.tables[index_table_2]

      # find person in table 2 to match seats quantity of person in table 1

      

      
      total_seats_2 = 0
      persons2 = []
      for person in table2.persons:
        seat = person.seats
        if seats1 < (total_seats_2 + seat):
          continue
        elif seats1 == total_seats_2:
          break
        else:
          persons2.append(person)
          total_seats_2 += seat
      
      # exchange people
      table1.removePerson(person1)
      for p2 in persons2:
        table2.removePerson(p2)
        table1.addPerson(p2)
      table2.addPerson(person1)
      '''

    self.updateScore()

