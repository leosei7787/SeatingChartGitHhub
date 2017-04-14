#!/usr/bin/python

#### Parse CSV into Guests ######
def getGuests(file,truncate):
  guests = []
  total_guests = 0
  max_row = truncate
  with open(file, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    row_number = 0
    for row in reader:
      if row_number == 0:
        row_number += 1
        continue
      if row_number > max_row:
        break

      name = row[0]
      groups = row[1].split(",")
      seats = int(row[2])
      age = int(row[3])
      languages = row[4].split(",")

      temp = Person(name, seats, groups, languages, age)
      guests.append(temp)

      total_guests += seats
      row_number += 1
  return guests