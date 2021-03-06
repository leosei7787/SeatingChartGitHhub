#!/usr/bin/python3.6
import itertools
import statistics
import math

###### CLASS TABLE ######
class Table(object):
  'Define a Table'
  weight_config = {}

  def __init__(self,id,seats,weight_config):
    self.id = id
    self.seats = seats
    self.persons = []
    self.weight_config = weight_config

  def setPersons(self,persons):
    self.persons = persons
  
  def addPerson(self,person,debug=False):
    if self.getFreeSeats() < person.seats:
      if debug == True:
        print("no room for %s at table %d"%(person.name,self.id))
      return False
    else:
      self.persons.append(person)
      if debug == True:
        print("added %s at table %d"%(person.name,self.id))
      return True

  def removePerson(self,person):
    temp_persons = []
    for p in self.persons:
      if p.name != person.name:
        temp_persons.append(p)
    self.persons = temp_persons

  def getUsedSeats(self):
    seats = 0
    # check noone is at the table
    if len(self.persons) == 0:
      return seats
    # loop over persons to sum seats.
    for person in self.persons:
        seats += person.seats
    return seats

  def getFreeSeats(self):
    return ( self.seats - self.getUsedSeats() )

  # return list of unique groups
  def getGroups(self):
    total_group = []
    for person in self.persons:
      total_group += person.groups
    return set(total_group)

  # return list of unique languages at the table
  def getLanguages(self):
    total_languages = []
    for person in self.persons:
      total_languages += person.languages
    return set(total_languages)

  def emptyTable(self):
    self.persons = []

  def getScore(self):
    table_score = 0
    if len(self.persons) == 0:
      return table_score

    #Iterate over each unique set of persons (pa,pb)
    for pa,pb in itertools.combinations(self.persons,2):
      # Age weight from config divided by age diff (so smaller delta will yield higher score)
      delta = 1 + abs(pa.age - pb.age) 
      age_score = int(self.weight_config["age"]) / delta 

      # language weight from config if at least one similar language, 0 otherwise
      language_score = 0
      if not set(pa.languages).isdisjoint(pb.languages) is True: 
        language_score = self.weight_config["language"]
      
      # group weight from config if at least one similar group, 0 otherwise
      group_score = 0
      if not set(pa.groups).isdisjoint(pb.groups) is True: 
        group_score = self.weight_config["group"]

      # check nogo list
      for nogo in self.weight_config["nogo_list"]:
        if pa.name in nogo and pb.name in nogo:
          return 0

      # Protect against big age delta in diff group
      if delta > self.weight_config["max_age_diff"] and group_score == 0:
        return 0

      multiplier = (pa.seats * pb.seats) 
      table_score += multiplier * (age_score + language_score + group_score )

    '''
    # add boost score for each person with more than 1 seat (to account for )
    for couple in self.persons:
      if couple.seats > 1:
        table_score += couple.seats * (int(self.weight_config["age"])+self.weight_config["language"]+self.weight_config["group"])
    '''
    # normalize by number of person to smooth for couple and various sizes
    total_score = 10 * table_score / len(self.persons)
    return total_score

  def toString(self):
    temp = "table: %d (%d / %d) - Score %d: "%(self.id,self.getUsedSeats(), self.seats, self.getScore())
    return temp

  def toStringList(self):
    temp = "table: %d (%d / %d) - Score %d: "%(self.id,self.getUsedSeats(), self.seats, self.getScore())
    p = []
    for person in self.persons:
      p.append(person.toString())
    temp += ",".join(p)
    return temp  


  def toStringDebug(self):
    temp = "\ntable: %d (%d / %d), score: %.d:  "%(self.id,self.getUsedSeats(), self.seats, self.getScore())
    #temp += "\n groups:%s langs: %s\n\n"%(",".join(self.getGroups()), ",".join(self.getLanguages()))
    for person in self.persons:
        temp += "\n%s, "%person.toStringDebug()
    temp +"\n"
    return temp

