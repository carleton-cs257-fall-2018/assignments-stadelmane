import csv

with open("books.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row[1])