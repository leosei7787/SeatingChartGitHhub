#!/usr/bin/python
from random import randint
import json
from pprint import pprint

def setUsersOnTable(persons,tables,verbose=False):
  persons = sorted(persons, key=lambda obj: obj.seats,reverse=True)
  # randomly add guests to table
  total_table = len(tables)
  for person in persons:
    # pick a random table
    selected_table = randint(0,total_table-1)
    table = tables[selected_table]
    # add to table
    added = table.addPerson(person,verbose)
    if added != True:
      tried = selected_table
      selected_table = (selected_table + 1) % total_table
      while tried != selected_table and added != True:
       table = tables[selected_table]
       added = table.addPerson(person,verbose)
       selected_table = (selected_table + 1) % total_table
  return tables


def getNogo(file):
  with open(file) as data_file:    
    return json.load(data_file)