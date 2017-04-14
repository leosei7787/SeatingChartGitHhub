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



  def updateScore(self):
    table_score = 0
    #Iterate over each unique set of persons (pa,pb)
    for pa,pb in itertools.combinations(self.persons,2):
      # remove from 1 from score on age diff (weighted by configuration)
      age_score = -int(abs(pa.age - pb.age) / self.weight_config["age"])

      # add config if similar language, 0 otherwise
      language_score = 0
      if not set(pa.languages).isdisjoint(pb.languages) is True: 
        language_score = self.weight_config["language"]
      

      # add config if similar group
      group_score = 0
      if not set(pa.groups).isdisjoint(pb.groups) is True: 
        group_score = self.weight_config["group"]

      # check nogo list
      nogo_score = 0
      for nogo in self.weight_config["nogo_list"]:
        if pa.name in nogo and pb.name in nogo:
          nogo_score = -self.weight_config["nogo"]          

      multiplier = (pa.seats + pb.seats) 
      table_score += multiplier * (age_score + language_score + group_score + nogo_score)
    self.score = table_score
    return self.score

  def toString(self):
    temp = "table: %d (%d / %d) - Score %d: "%(self.id,self.getUsedSeats(), self.seats, self.score)
    return temp

  def toStringDebug(self):
    temp = "table: %d (%d / %d), score: %.d:  "%(self.id,self.getUsedSeats(), self.seats, self.score)
    #temp += "\n groups:%s langs: %s\n\n"%(",".join(self.getGroups()), ",".join(self.getLanguages()))
    for person in self.persons:
        temp += "\n%s, "%person.toStringDebug()
    temp +"\n"
    return temp





'''
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
'''


