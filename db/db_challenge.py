"""
Defines database operations to do with challenges.
"""

class Challenge:

	"""
	Fetch all information about all challenges.
	"""
	def getChallengeInfos(self):
		res = self.query("SELECT * FROM Challenge")
		return res

	"""
	Fetch all information about a challenge by name.
	"""
	def getChallengeInfo(self, challengeName):
		res = self.query("SELECT * FROM Challenge WHERE challengeName = ?", [
			challengeName
		], one = True)
		return res

	"""
	Fetch the names of all challenges.
	"""
	def getChallengeNames(self):
		res = self.query("SELECT challengeName FROM Challenge")
		# list comprehension to convert dict to a simple list, for example:
		# [{"username": 1}, {"username": 2}, {"username": 3}] becomes [1, 2, 3]
		res = [d.get("challengeName") for d in res]
		return res

	"""
	Get the people who have solved a challenge.
	"""
	def getSolves(self, challengeName):
		res = self.query("SELECT username FROM ChallengeSolve WHERE challengeName = ?", [
			challengeName
		])
		# list comprehension to convert dict to a simple list of usernames, for example:
		# [{"username": 1}, {"username": 2}, {"username": 3}] becomes [1, 2, 3]
		res = [d.get("username") for d in res]
		return res

	"""
	Get the user who has first blooded a particular challenge.
	"""
	def getBlood(self, challengeName):
		res = self.query("SELECT username FROM ChallengeSolve WHERE firstBlood = true AND challengeName = ?", [
			challengeName
		], one=True)
		if not res: return None # if no such user exists, return nothing
		return res.get("username")

	"""
	Add a user solve to a challenge.
	"""
	def addSolve(self, challengeName, username, firstBlood):
		self.query("INSERT INTO ChallengeSolve (challengeName, username, firstBlood) VALUES (?, ?, ?)", [
			challengeName,
			username,
			firstBlood # boolean representing if that solve was the first solve or not
		])
		return
