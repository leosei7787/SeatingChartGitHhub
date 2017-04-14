#!/usr/bin/python3.6
########## CLASS PERSON #########
class Person:
  'Define a person'

  def __init__(self, name, seats, groups, languages, age):
    self.name = name
    self.seats = seats
    self.groups = groups
    self.languages = languages
    self.age = age

  def toString(self):
    return self.name+" ("+str(self.seats)+")"

  def __eq__(self, other):
    return self.name == other.name  
