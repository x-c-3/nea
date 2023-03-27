# /web.py
# Routing for the frontend

from flask import *
from middlewares import * # for login required function

web = Blueprint(
	"web", # the name, which will just be web
	__name__, # the import name
)

# Self-explanatory routes that render HTML for login, register, etc...
@web.route("/login")
def login():
	return render_template("login.jinja2")

@web.route("/register")
def register():
	return render_template("register.jinja2")

@web.route("/scoreboard")
def scoreboard():
	return render_template("scoreboard.jinja2")

@web.route("/")
def index():
	return render_template("index.jinja2")

@web.route("/user/<username>")
def profile(username):
	return render_template("profile.jinja2")

@web.route("/challenges")
@webLoginRequired
def challenges():
	return render_template("challenges.jinja2")

@web.route("/challenge/<challengeName>")
@webLoginRequired
def challenge(challengeName):
	return render_template("challenge.jinja2")

@web.route("/courses")
@webLoginRequired
def courses():
	return render_template("courses.jinja2")

@web.route("/course/<courseName>")
@webLoginRequired
def course(courseName):
	return render_template("course.jinja2")

@web.route("/logout")
def logout():
	session.clear()
	return redirect("/")