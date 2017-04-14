#!/usr/bin/python
import csv
from ClassPerson import Person

#### Parse CSV into Guests ######
def getGuests(file,header,truncate):
  guests = []
  with open(file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    row_number = 0
    for row in reader:
      #Skip header
      if row_number == 0:
        row_number += 1
        continue
      #Stop at truncate
      if row_number > truncate:
        break
      row_number += 1
      
      name = row[header["name"]]
      groups = row[header["groups"]].split(",")
      seats = int(row[header["seats"]])
      age = int(row[header["age"]])
      languages = row[header["language"]].split(",")

      guests.append( Person(name, seats, groups, languages, age) )

  return guests