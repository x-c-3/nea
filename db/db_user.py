"""
Defines database operations to do with the user.
"""

from hashlib import sha256
from datetime import datetime
from consts import *

class User:
	"""
	Returns if a given username exists in the database.
	"""
	def userExists(self, username) -> bool:
		res = self.query("SELECT username FROM User WHERE username = ?", [username])
		if res: return True

		# Reaching here means no username was found
		return False

	"""
	Returns a boolean corresponding to if a user's password matches with the hash stored in the database.
	"""
	def loginUser(self, username, password):
		res = self.query("SELECT username FROM User WHERE username = ? AND password = ?", [
			username,
			sha256(bytes(password, "utf-8")).hexdigest() # Hashing the password
		], one = True)
		if res:
			# successful login
			return True

		# Reaching here means the password does not match
		return False

	"""
	Registers a user with default stats.
	Set their streak to 1 and the last time they logged in to now.
	"""
	def registerUser(self, username, password) -> None:
		self.query("INSERT INTO User (username, password, lastLogin, lastStreakLogin, streak) VALUES (?, ?, ?, ?, ?)", [
			username,
			sha256(bytes(password, "utf-8")).hexdigest(), # Hashing the password for secure storage
			datetime.now().strftime(DATE_FORMAT),
			datetime.now().strftime(DATE_FORMAT),
			1
		])
		return

	"""
	Get and set the last time when the user logged in and it counted towards their login streak.
	"""
	def getLastStreakLogin(self, username):
		res = self.query("SELECT lastStreakLogin FROM User WHERE username = ?", [username], one = True)
		if not res: return None
		return res.get("lastStreakLogin")

	def setLastStreakLogin(self, username, lastStreakLogin):
		self.query("UPDATE User SET lastStreakLogin = ? WHERE username = ?", [
			lastStreakLogin,
			username
		])
		return

	"""
	Get and set the last time when the user logged in at all.
	"""
	def getLastLogin(self, username):
		res = self.query("SELECT lastLogin FROM User WHERE username = ?", [username], one = True)
		if not res: return None
		return res.get("lastLogin")

	def setLastLogin(self, username, lastLogin):
		self.query("UPDATE User SET lastLogin = ? WHERE username = ?", [
			lastLogin,
			username
		])
		return

	"""
	Get and set the user's login streak.
	"""
	def getStreak(self, username):
		res = self.query("SELECT streak FROM User WHERE username = ?", [username], one = True)
		if not res: return None
		return res.get("streak")

	def setStreak(self, username, streak):
		self.query("UPDATE User SET streak = ? WHERE username = ?", [
			streak,
			username
		])
		return

	"""
	Get the names of challenges that this user has first blooded.
	"""
	def getBloods(self, username):
		res = self.query("SELECT challengeName FROM ChallengeSolve WHERE username = ? AND firstBlood = true", [
			username
		])
		# list comprehension to convert dict to a simple list, for example:
		# [{"username": 1}, {"username": 2}, {"username": 3}] becomes [1, 2, 3]
		return [d.get("challengeName") for d in res]

	"""
	Get the total number of points of a specific user.
	"""
	def getUserPoints(self, username):
		res = self.query("""
			SELECT SUM(Challenge.points) AS totalPoints FROM Challenge, ChallengeSolve
			WHERE Challenge.challengeName = ChallengeSolve.challengeName
			AND ChallengeSolve.username = ?;
		""", [ username ], one=True).get("totalPoints")

		# if the user hasn't solved any challenges, no records in ChallengeSolve will exist for them
		# so None will be returned - in this case, return 0
		if res == None: return 0

		return res

	"""
	Get a list of dictionaries of usernames and points of all the users on the platform.
	"""
	def getAllUserPoints(self):
		res = self.query("""
			SELECT User.username, (
				SELECT SUM(Challenge.points) FROM Challenge, ChallengeSolve
				WHERE Challenge.challengeName = ChallengeSolve.challengeName
				AND ChallengeSolve.username = User.username
			) AS totalPoints FROM User
		""")

		for record in res:
			# if the user hasn't solved any challenges, no records in ChallengeSolve will exist for them
			# so None will be returned - in this case, set 0
			if record.get("totalPoints") == None: record["totalPoints"] = 0

		return res

	"""
	Get the names of challenges that this user has solved.
	"""
	def getSolvedChallengeNames(self, username):
		res = self.query("SELECT challengeName FROM ChallengeSolve WHERE username = ?", [
			username
		])
		# list comprehension to convert dict to a simple list, for example:
		# [{"username": 1}, {"username": 2}, {"username": 3}] becomes [1, 2, 3]
		return [d.get("challengeName") for d in res]

	"""
	Get the courses a user has solved.
	"""
	def getSolvedCourseNames(self, username):
		res = self.query("SELECT courseName FROM CourseSolve WHERE username = ?", [
			username
		])
		return res