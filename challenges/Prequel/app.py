from flask import *
from sqlite3 import connect, OperationalError
import re
import sys

app = Flask(__name__)

# refresh the template cache whenever templates are required in order to speed up development
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.before_first_request
def init_db():

	# connect to the database
	db = connect("database.db")
	cursor = db.cursor()

	# create the Movie table. each movie is described by its title and description.
	# hidden is required here in order to hide some fields so that SQL injection is viable.
	cursor.execute("DROP TABLE IF EXISTS Movie")
	cursor.execute("""CREATE TABLE Movie (
		id INTEGER PRIMARY KEY,
		title VARCHAR(255),
		description VARCHAR(255),
		hidden BOOL
	)""")
	cursor.execute("INSERT INTO Movie VALUES (1, 'The Flag Movie', 'The main character, ctf{unsanitised_sql_me4ns_d4nger}, is traded for points.', true)")
	cursor.execute("INSERT INTO Movie VALUES (2, 'Made-Up Movie', 'Characters are forced to make up a movie as they go along.', false)")
	cursor.execute("INSERT INTO Movie VALUES (3, 'Craftmine', 'In a dystopian future, it''s craft or be mined.', false)")
	cursor.execute("INSERT INTO Movie VALUES (4, 'Hanon', 'A struggling pianist writes influential piano exercises.', false)")
	cursor.execute("INSERT INTO Movie VALUES (5, 'Naijan', 'Naijan the Ninja has internal strife.', false)")
	cursor.execute("INSERT INTO Movie VALUES (6, 'A Long Movie', 'This movie lasts for 9 hours.', false)")
	cursor.execute("INSERT INTO Movie VALUES (7, 'Luigi', 'A destitute green plumber steals from the rich and gives back to the rich.', false)")
	cursor.execute("INSERT INTO Movie VALUES (8, 'The C Movie', 'The sequel to The Bee Movie. Jerry Seinfeld plays the Atlantic.', false)")

	# save changes
	db.commit()
	db.close()

def search(title):

	# connect to the db
	db = connect("database.db")
	cursor = db.cursor()

	# set up query
	# direct insertion is needed for SQL injection
	query = f"""SELECT title, description FROM Movie WHERE title LIKE "%{title}%" AND hidden = false;"""

	# execute query
	cursor.execute(query)
	res = cursor.fetchall()

	# save changes
	db.commit()
	db.close()

	return res, query

@app.route("/")
def index():

	# get arguments
	title = request.args.get("title")

	# if no title was provided, then simply show all of the movies
	if not title:
		all_movies, _ = search("%")
		return render_template("index.html", res = all_movies)

	# otherwise, try getting movies from the backend
	try:
		res, query = search(title)
	except OperationalError:
		return render_template("index.html", error = "There was an error while executing your query!")

	return render_template("index.html", res = res, query = query)


if len(sys.argv) == 2: app.run("0.0.0.0", sys.argv[1])
else: app.run("0.0.0.0", 3000)