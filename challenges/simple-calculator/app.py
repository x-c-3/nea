from flask import *
from sqlite3 import connect
import re
import sys

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

def fetchFromCache(calculation):
	# Get the calculation from cache.

	db = connect("database.db")
	cursor = db.cursor()

	print(calculation)
	cursor.execute("SELECT result FROM cache WHERE calculation = '" + calculation + "'")
	res = cursor.fetchall()
	if res: return res[0][0] # if cached, return it
	else: return None # otherwise, nothing

	db.commit()
	db.close()

def addToCache(calculation, res):
	# Add the calculation to cache for future quick access.

	db = connect("database.db")
	cursor = db.cursor()

	cursor.execute("INSERT INTO cache VALUES ('" + calculation + "', '" + res + "')")

	db.commit()
	db.close()

@app.before_first_request
def init_db():

	db = connect("database.db")
	cursor = db.cursor()

	cursor.execute("DROP TABLE IF EXISTS Cache")
	cursor.execute("""CREATE TABLE Cache (
		calculation VARCHAR(255) PRIMARY KEY,
		result VARCHAR(255)
	)""")
	cursor.execute("INSERT INTO Cache VALUES ('flag', 'ctf{not_s0_simple_solut1on_g00d_j0b}')")

	db.commit()
	db.close()

@app.route("/calculate")
def calculate():

	number1 = request.args.get("number1")
	operation = request.args.get("operation")
	number2 = request.args.get("number2")

	if not number1.isdigit() or not number2.isdigit():
		return render_template("index.html", error = "Invalid input")

	operation = re.sub(r"[a-zA-Z]", "", operation)
	calculation = number1 + operation + number2

	try:
		res = fetchFromCache(calculation)
	except:
		return render_template("index.html", error = "Something went wrong when fetching from cache")

	if res: return render_template("result.html", result = res)
	else:

		number1 = int(number1)
		number2 = int(number2)

		if operation == "+": res = number1 + number2
		elif operation == "-": res = number1 - number2
		elif operation == "*": res = number1 * number2
		elif operation == "/": res = number1 / number2

		try:
			addToCache(calculation, str(res))
		except: pass # something went wrong while adding the operation to cache, but that's ok

		return render_template("result.html", result = res)

@app.route("/")
def index():
	return render_template("index.html")

if len(sys.argv) == 2: app.run("0.0.0.0", sys.argv[1])
else: app.run("0.0.0.0", 3000)