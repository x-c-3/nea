import sqlite3
import yaml
import json

levels = yaml.safe_load(open("data/levels.yaml"))["levels"]
courses = yaml.safe_load(open("data/courses.yaml"))["courses"]
challenges = yaml.safe_load(open("data/challenges.yaml"))["challenges"]

db = sqlite3.connect("db.db")
cursor = db.cursor()

cursor.execute("DELETE FROM Course")
cursor.execute("DELETE FROM Level")
cursor.execute("DELETE FROM Challenge")

cursor.executemany("INSERT INTO Course (courseName, shortDesc) VALUES (:courseName, :shortDesc)", courses)

for course in levels:
	courseName = course["courseName"]
	levels = course["levels"]
	for level in levels:
		level["infos"] = json.dumps(level["infos"])

	cursor.executemany(f"""INSERT INTO Level(courseName, levelNo, infos) VALUES ("{courseName}", :levelNo, :infos)""", levels)

cursor.executemany("""INSERT INTO Challenge(challengeName, description, shortDesc, difficulty, points, category, flag, source, courseName, levelNo) VALUES (:challengeName, :description, :shortDesc, :difficulty, :points, :category, :flag, :source, :courseName, :levelNo)""", challenges)


db.commit()
db.close()