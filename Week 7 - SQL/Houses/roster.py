import sys
import csv
from cs50 import SQL


# exits if there are incorrect number of args
if (len(sys.argv) != 2):
    print("Usage: python.py import.py House_Name")
    sys.exit()

# declarations
db = SQL("sqlite:///students.db")
house = sys.argv[1]

# creates a list of dictionary
rows = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

# prints the output
for row in rows:
    if not row['middle']:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")