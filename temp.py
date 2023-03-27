from flask import *

# for static challenges (eg JavaScript challenges), templating is not necessary - simply serve static files
app = Flask(__name__, static_url_path="/", static_folder="html")

# for requests to just /, return the index page
@app.route("/")
def index(): return send_from_directory("html", "index.html")

# serve the app on port 3000
app.run("0.0.0.0", 3000)