#!/usr/bin/python3

import datetime
import csv
import sys
import math

timefmt = "%Y-%m-%d %H:%M:%S"
timefmt_days = "%Y-%m-%d"
timefmt_weeks = "%G-W%V" # Note that this uses the ISO 8601 year and week to
                         # ommit a "week 0".

start_date = datetime.datetime.strptime("2019-04-09 00:00:00", timefmt)

dictionary_input = { }

def sum_per_day():
    with open(sys.argv[2]) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            if row[0] not in dictionary_input:
                dictionary_input[row[0]] = {}

                # Initialize the dictionary with each day
                current_date = datetime.datetime.today()

                days = (current_date - start_date).days
                i = 0
                while i <= days:
                    dictionary_input[row[0]][datetime.datetime.strftime(start_date + datetime.timedelta(days=i), "%Y-%m-%d")] = datetime.timedelta(0)
                    i = i + 1

            rowdate = datetime.datetime.strftime(datetime.datetime.strptime(row[1], timefmt), "%Y-%m-%d")
            duration = datetime.datetime.strptime(row[2], timefmt) - datetime.datetime.strptime(row[1], timefmt)

            dictionary_input[row[0]][rowdate] += duration

def sum_per_week():
    with open(sys.argv[2]) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            if row[0] not in dictionary_input:
                dictionary_input[row[0]] = {}

                # Initialize the dictionary with each week
                current_date = datetime.datetime.today()

                weeks = math.ceil((current_date - start_date).days / 7.0)
                i = 0
                while i <= weeks:
                    dictionary_input[row[0]][datetime.datetime.strftime(start_date + datetime.timedelta(weeks=i), timefmt_weeks)] = datetime.timedelta(0)
                    i = i + 1

            print(dictionary_input)

            rowdate = datetime.datetime.strftime(datetime.datetime.strptime(row[1], timefmt), timefmt_weeks)
            duration = datetime.datetime.strptime(row[2], timefmt) - datetime.datetime.strptime(row[1], timefmt)

            dictionary_input[row[0]][rowdate] += duration

if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " [week/day] [input.csv]")
    exit(-1)

if sys.argv[1] == "day":
    sum_per_day()
elif sys.argv[1] == "week":
    sum_per_week()
else:
    print("Usage: " + sys.argv[0] + " [week/day] [input.csv]")

# This contains a dictionary with all categories, each category contains a
# dictionary with a timedelta object for each date.
print(dictionary_input)

for category in dictionary_input:
    filename = category + ".csv"

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')

        for row in dictionary_input[category]:
            csvrow = [row, str(round(dictionary_input[category][row].total_seconds() / 60))]
            print(csvrow)
            csvwriter.writerow(csvrow)
