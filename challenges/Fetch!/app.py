from flask import *
import sys

# Static app with static files in ./html
app = Flask(__name__, static_url_path="/", static_folder="html")

@app.route("/")
def index(): return send_from_directory("html", "index.html")

@app.route("/giveflag", methods = ["POST"])
def giveflag():

	flag = request.json.get("flag")

	# If flag is set to true, then return the flag
	if flag: return Response(f"""\
		flag={flag}
		Well done! Here's your flag: ctf{{Web_API_w1zard}}\
	""".replace("\t", ""), headers = {"content-type": "text/plain"})

	# Otherwise, tell the user that flag is false
	else: return Response(f"""\
		flag={flag}
		Okay then, no flag...\
	""".replace("\t", ""), headers = {"content-type": "text/plain"})

if len(sys.argv) == 2: app.run("0.0.0.0", sys.argv[1])
else: app.run("0.0.0.0", 3000)