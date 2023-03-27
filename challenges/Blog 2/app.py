from flask import *
import sys
from sqlite3 import connect, OperationalError
import os

app = Flask(__name__, static_url_path="/", static_folder="html")

@app.before_first_request
def init_db():

	db = connect("database.db")
	cursor = db.cursor()

	cursor.execute("DROP TABLE IF EXISTS User")
	cursor.execute("""CREATE TABLE User (
		username VARCHAR(255) PRIMARY KEY,
		password VARCHAR(255)
	)""")
	cursor.execute("INSERT INTO User VALUES ('AzureDiamond', 'hunter2')")
	cursor.execute("INSERT INTO User VALUES ('another_user', 'password')")
	cursor.execute("INSERT INTO User VALUES ('ctf{5ql_4nd_jav4scr1pt_sup3rst4r}', ?)", [ os.urandom(8).hex() ])
	cursor.execute("INSERT INTO User VALUES ('Not_The_Flag', 'o7flagless')")
	cursor.execute("INSERT INTO User VALUES ('YetAnotherUser', 'password1')")

	db.commit()
	db.close()

@app.route("/login", methods = ["POST"])
def login():

	username = request.json.get("username")
	password = request.json.get("password")

	if not all([username, password]): return {
		"error": "One or more parameters missing"
	}, 400

	# create connection and cursor
	db = connect("database.db")
	cursor = db.cursor()

	# get the user
	query = f"SELECT username FROM User WHERE username = '{username}' AND password = '{password}'"

	try:
		cursor.execute(query)
	except OperationalError:
		return {
			"error": "Something went wrong while executing the SQLite query!",
			"query": query
		}, 400

	data = cursor.fetchall()

	if data: logged_in_user = data[0][0]
	else: return {
		"error": "Invalid credentials"
	}, 403

	return {
		"success": f"Welcome back, {logged_in_user}!"
	}, 200

@app.route("/register", methods = ["POST"])
def register():

	username = request.json.get("username")
	password = request.json.get("password")

	if not all([username, password]): return {
		"error": "One or more parameters missing"
	}, 400

	# create connection and cursor
	db = connect("database.db")
	cursor = db.cursor()

	# reject if username not unique
	try:
		query = f"SELECT username FROM users WHERE username = '{username}'"
		cursor.execute(query)
		data = cursor.fetchall()
		if data: return {
			"error": "Username taken"
		}, 400

		query = f"INSERT INTO users(username, password) VALUES ('{username}', '{password}')"
		cursor.execute(query)
	except OperationalError:
		return {
			"error": "Something went wrong while executing the SQLite query!",
			"query": query
		}, 400

	db.commit()
	db.close()

	return {
		"success": "Successfully registered an account!"
	}, 200

@app.route("/")
def index(): return send_from_directory("html", "index.html")

if len(sys.argv) == 2: app.run("0.0.0.0", sys.argv[1])
else: app.run("0.0.0.0", 3000)