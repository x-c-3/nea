from flask import *
import sys
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/curl")
def curl():

	url = request.args.get("url")

	try:
		# run cURL to get the contents of the page, capturing output
		process = subprocess.run(["curl", url], capture_output=True)
	except:
		return render_template("index.html", error="Something went wrong, please check your input")

	# the content has to be decoded as latin-1, as some sites/files (eg PNG) will return bytes that cannot be decoded into utf-8, which will throw an error
	return render_template("result.html", content=process.stdout.decode("latin-1"))

@app.route("/flag")
def flag():
	if request.remote_addr != "127.0.0.1": return "Nice try :)"
	return "ctf{s3rver_side_superst4r}"

if len(sys.argv) == 2: app.run("0.0.0.0", sys.argv[1])
else: app.run("0.0.0.0", 3000)