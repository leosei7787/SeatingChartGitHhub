#!/usr/bin/python3.6
import itertools
import statistics

###### CLASS TABLE ######
class Table:
  'Define a Table'
  weight_config = {}

  def __init__(self,id,seats,weight_config):
    self.id = id
    self.seats = seats
    self.persons = []
    self.weight_config = weight_config
    self.score = 0


  def setPersons(self,persons):
    self.persons = persons
    self.updateScore()
  
  def addPerson(self,person,debug=False):
    if self.getFreeSeats() < person.seats:
      if debug == True:
        print("no room for %s at table %d"%(person.name,self.id))
      return False
    else:
      self.persons.append(person)
      if debug == True:
        print("added %s at table %d"%(person.name,self.id))
    self.updateScore()
    return True

  def removePerson(self,person):
    temp_persons = []
    for p in self.persons:
      if p.name != person.name:
        temp_persons.append(p)
    self.persons = temp_persons
    self.updateScore()


  def getUsedSeats(self):
    seats = 0
    if self.persons != []:
      for person in self.persons:
        seats += person.seats
    return seats

  def getFreeSeats(self):
    return self.seats - self.getUsedSeats()

  def getGroups(self):
    total_group = []
    for person in self.persons:
      total_group += person.groups
    return set(total_group)

  def getLanguages(self):
    total_languages = []
    for person in self.persons:
      total_languages += person.languages
    return set(total_languages)

  def getScoreGroup(self):
    group_couple = 0
    couples = 0
    # Compare each couple of people only once.
    for pa, pb in itertools.combinations(self.persons, 2):
      la = pa.groups
      lb = pb.groups
      couples += pa.seats+pb.seats
      # Check if there is at least one commong language
      if not set(la).isdisjoint(lb) is True:
        # Increase number of people that can speak, weighted by seat used.
        group_couple += pa.seats+pb.seats
    
    # Normalize to get score of 0 - 1
    score = 0
    if couples > 0:
      score = group_couple / float(couples)
    return score


  def getFreeSeatsScore(self):
    return self.getUsedSeats() /  float(self.seats)

  def getScoreLanguage(self):
    speaking_couple = 0
    couples = 0
    # Compare each couple of people only once.
    for pa, pb in itertools.combinations(self.persons, 2):
      la = pa.languages
      lb = pb.languages
      couples += pa.seats+pb.seats
      # Check if there is at least one commong language
      if not set(la).isdisjoint(lb) is True:
        # Increase number of people that can speak, weighted by seat used.
        speaking_couple += pa.seats+pb.seats
    # Normalize to get score of 0 - 1

    score = 0
    if couples > 0:
      score = speaking_couple / float(couples)
    return score

  def getScoreAge(self):
    ages = []
    for person in self.persons:
      temp = [person.age] * person.seats
      ages += temp
    score = 0
    if len(ages)>1:
      #STD divided in 5 years buckets to smooth things
      stdev = statistics.stdev(ages) / 5
      if stdev>0:
        score = 1 /float(stdev)
    return score



  def updateScore(self):
    score = self.weight_config["group"] * self.getScoreGroup() 
    score += self.weight_config["language"] * self.getScoreLanguage() 
    score += self.weight_config["age"] * self.getScoreAge()
    score += self.weight_config["seat"]* self.getFreeSeatsScore()
    #TODO: If table contains two person in NoGo tuple, reset score to 0
    self.score = score

  def toString(self):
    temp = "table: %d (%d / %d) - Score %.4f: "%(self.id,self.getUsedSeats(), self.seats, self.score)
    for person in self.persons:
        temp += "%s, "%person.toString()
    return temp

  def toStringDebug(self):
    temp = "table: %d (%d / %d), score: %.4f (age %.4f lang %.4f groups %.4f seat %.4f): "%(self.id,self.getUsedSeats(), self.seats, self.score, self.getScoreAge(), self.getScoreLanguage(), self.getScoreGroup(), self.getFreeSeatsScore())
    #temp += "\n groups:%s langs: %s\n\n"%(",".join(self.getGroups()), ",".join(self.getLanguages()))
    for person in self.persons:
        temp += "\n%s, "%person.toString()
    temp +"\n"
    return temp