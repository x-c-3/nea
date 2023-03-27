from datetime import datetime, timedelta
from consts import *
from db import db
from middlewares import *

def wrap_user(api):

	@api.route("/login", methods = ["POST"])
	def login():
		"""
		API login route.
		---
		parameters:
			-	name: username
				in: formbody
				type: string
				required: true
				description: Username to login with
			-	name: password
				in: formbody
				type: string
				required: true
				description: Password to login with
		"""
		username = request.form.get("username", "") # Defaults to empty string if not supplied
		password = request.form.get("password", "")
		if db.loginUser(username, password): # Successful login

			# set username on the session if successful
			session["username"] = username

			"""
			When a user logs in, updates their login streak accordingly
			"""

			lastStreakLogin = datetime.strptime(
				db.getLastStreakLogin(username),
				DATE_FORMAT
			) # stored in the db as a date string - parse it using the global format

			now = datetime.now()

			# set their last login
			db.setLastLogin(username, datetime.strftime(now, DATE_FORMAT))

			if now > lastStreakLogin + timedelta(hours = 48): # logged in after streak is over
				db.setStreak(username, 1)
				db.setLastStreakLogin(username, datetime.strftime(now, DATE_FORMAT))
			elif now > lastStreakLogin + timedelta(hours = 24): # logged in to maintain streak
				db.setStreak(username, db.getStreak(username) + 1) # increment the streak
				db.setLastStreakLogin(username, datetime.strftime(now, DATE_FORMAT))
			else: # already claimed streak
				pass

			return {
				"message": "Logged in!"
			}, 200
		else: # Bad login
			return {
				"message": "Wrong or missing credentials"
			}, 400

	@api.route("/register", methods = ["POST"])
	def register():
		"""
		API register route.
		---
		parameters:
			-	name: username
				in: formbody
				type: string
				required: true
				description: Username to register with
			-	name: password
				in: formbody
				type: string
				required: true
				description: Password to register with
		"""
		username = request.form.get("username", "") # Defaults to empty string if not supplied
		password = request.form.get("password", "")

		# Username must be between 3-30 characters long
		if not (3 <= len(username) <= 30): return {
			"message": "Username must be between 3-30 characters long"
		}, 400

		# Password must be at least 8 characters long, for security
		if not len(password) >= 8: return {
			"message": "Password must be at least 8 characters long"
		}, 400

		if not db.userExists(username): # Can register this username
			db.registerUser(username, password)
			return {
				"message": "Account created! Please log in."
			}, 200
		else: # User already exists
			return {
				"message": "Username exists already"
			}, 400

	@api.route("/user/<username>", methods = ["GET"])
	@apiLoginRequired
	def getStats(username):
		"""
		Interface to the the specific stats of a user.
		Stats include:

		- streak
		- lastLogin
		- lastStreakLogin
		- points
		- firstBloods

		---
		parameters:
			-	name: username
				in: path
				type: string
				required: true
		"""

		if not db.userExists(username): return {
			"message": "User does not exist"
		}, 400

		stats = {
			"streak": db.getStreak(username),
			"lastLogin": db.getLastLogin(username),
			"lastStreakLogin": db.getLastStreakLogin(username),
			"points": db.getUserPoints(username),
			"firstBloods": db.getBloods(username)
		}
		return stats, 200

	@api.route("/user", methods = ["GET"])
	@apiLoginRequired
	def getSelfUsername():
		"""
		Get the logged-in user's username.
		"""
		return {"username": session["username"]}, 200