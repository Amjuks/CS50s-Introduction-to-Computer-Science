import sys
import csv
from cs50 import SQL


# exits if there are incorrect number of arguements
if (len(sys.argv) != 2):
    print("Usage: python.py import.py file.csv")
    sys.exit()

# exits if it isnt a csv file
if not (sys.argv[1].endswith('.csv')):
    print("Enter a .csv file")
    sys.exit()

# recreates the table and resets the index
db = SQL("sqlite:///students.db")
db.execute("DELETE FROM students")
db.execute('''DELETE FROM sqlite_sequence WHERE name = 'students' ''')

# opens the csv file to read its contents
with open(sys.argv[1], "r") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        name = row[0].split()

        if len(name) == 2:
            db.execute("INSERT INTO students (first, last, house, birth) VALUES (?, ?, ?, ?)", *name[:2], *row[1:])

        if len(name) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", *name[:3], *row[1:])