import sys
import csv
import re


def main():

    # check if there are correct number of args
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit()

    # opens the database and stores it in a list
    csvfile = open(sys.argv[1], "r")
    reader = csv.reader(csvfile)
    data = list(reader)

    # declarations
    longest = []
    STR = []
    people = []
    l = []

    # stores the DNA pattern in a string
    seq_file = open(sys.argv[2], "r")
    sequence = seq_file.read()

    # finds the STRs
    for pattern in range(len(data[0]) - 1):

        # creates a list of all the patterns found
        l = re.findall(rf'(?:{data[0][pattern + 1]})+', sequence)

        # if the list it empty it exits
        if (len(l) == 0):
            print("No Match")
            sys.exit()

        longest.append(max(l, key=len))
        STR.append(int(len(longest[pattern])/len(data[0][pattern + 1])))

    # updates the database so that only the STRs are stored and saves the peoples name in another list
    for person in range(len(data) - 1):
        people.append(data[person + 1].pop(0))
    data.pop(0)

    for i in range(len(STR)):
        STR[i] = str(STR[i])

    if STR in data:
        for i in range(len(data)):
            if data[i] == STR:
                print(people[i])
                sys.exit()
    else:
        print("No match")


main()