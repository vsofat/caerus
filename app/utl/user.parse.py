import csv
import os
import json

DIR = os.path.dirname(__file__) + "/../static/data/"

users = {
    'teacher': list(),
    'admin': list(),
    'student': list()
}


def addUser(file, utype):
    with open(DIR + file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users[utype].append(row['email'])


addUser('teachers.csv', 'teacher')
addUser('students.csv', 'student')
addUser('admin.csv', 'admin')


with open(DIR + 'users.json', 'w') as writefile:
    json.dump(users, writefile, ensure_ascii=False)
