from flask import *
import sys

app = Flask(__name__, static_url_path="/", static_folder="html")

@app.route("/")
def index(): return send_from_directory("html", "index.html")

if len(sys.argv) == 2: app.run("0.0.0.0", sys.argv[1])
else: app.run("0.0.0.0", 3000)