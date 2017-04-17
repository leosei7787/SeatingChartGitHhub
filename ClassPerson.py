#!/usr/bin/python3.6
########## CLASS PERSON #########
class Person(object):
  'Define a person'

  def __init__(self, name, seats, groups, languages, age):
    self.name = name
    self.seats = seats
    self.groups = groups
    self.languages = languages
    self.age = age

  def toString(self):
    return "%s (%d)"%(self.name,self.seats)

  def toStringDebug(self):
    string =  "%s seats: %d, age:%d - Groups:[%s], languages: [%s]" \
              %(self.name,self.seats,self.age,",".join(self.groups), ",".join(self.languages))
    return string


  def __eq__(self, other):
    return self.name == other.name  
