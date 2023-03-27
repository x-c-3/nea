from middlewares import *
from db import db
from challenges import runningChallenges

def wrap_challenge(api):

	@api.route("/challenge/<challengeName>")
	@apiLoginRequired
	def getChallengeInfo(challengeName):
		"""
		Frontend interface to get challenge info.
		---
		parameters:
			-	name: challengeName
				in: path
				type: string
				required: true
				description: Name of the challenge to get info of
		"""
		info = db.getChallengeInfo(challengeName)
		if info == None: return {
			"message": "Challenge does not exist"
		}, 400

		del info["flag"] # Delete the flag

		# add challenge port
		for processData in runningChallenges:
			if processData["challengeName"] == challengeName:
				port = processData["port"]

		# add people who have solved the challenge
		solves = db.getSolves(challengeName)

		# add the first blooder
		firstBlood = db.getBlood(challengeName)

		info["port"] = port
		info["solves"] = solves
		info["firstBlood"] = firstBlood

		return info, 200

	@api.route("/challenges")
	@apiLoginRequired
	def getChallenges():
		"""
		Frontend interface to get all challenge names or infos.
		---
		parameters:
			-	name: username
				in: query
				type: str
				required: true
				description: User to get the solved challenges of.
			-	name: infos
				in: query
				type: str
				description: If given, return all infos instead
		"""

		username = request.args.get("username")
		infos = request.args.get("infos")

		# if a username is given, give all the challenge names that user has solved
		if username:
			res = db.getSolvedChallengeNames(username)
			return jsonify(res), 200

		# if infos is given, give all challenge infos
		if infos:
			challengeInfos = db.getChallengeInfos()

			for challengeInfo in challengeInfos:

				challengeName = challengeInfo["challengeName"]
				
				del challengeInfo["flag"] # Delete the flag

				# add challenge port
				for processData in runningChallenges:
					if processData["challengeName"] == challengeName:
						port = processData["port"]

				# add people who have solved the challenge
				solves = db.getSolves(challengeName)

				# add the first blooder
				firstBlood = db.getBlood(challengeName)

				challengeInfo["port"] = port
				challengeInfo["solves"] = solves
				challengeInfo["firstBlood"] = firstBlood

			return jsonify(challengeInfos), 200

		# otherwise, just return all challenge names
		else:
			return jsonify(db.getChallengeNames()), 200

	@api.route("/challenge/<challengeName>/flag", methods = ["POST"])
	@apiLoginRequired
	def submitFlag(challengeName):
		"""
		Check the flag of a challenge against a user's flag. If they match, then add a solve to that challenge if they haven't solved it already.

		If they were the first to solve the challenge, add a first blood solve.
		---
		parameters:
			-	name: flag
				in: formbody
				type: string
				required: true
			-	name: challengeName
				in: path
				type: string
				required: true
		"""

		flag = request.form.get("flag", "")

		challengeData = db.getChallengeInfo(challengeName) # data about the challenge
		if challengeData == None: return {
			"message": "Challenge does not exist!"
		}, 400
		correctFlag = challengeData.get("flag") # the flag for the challenge
		points = challengeData.get("points")
		difficulty = challengeData.get("difficulty")

		# Correct (flag matches)
		if flag == correctFlag:

			# Logic to check that they have not already solved the challenge

			# Get all users who solved the challenge
			users = db.getSolves(challengeName)
			username = session["username"]

			# if the user does exist, they have already solved, so do nothing
			if username in users:
				return {
					"message": "You have solved this challenge already!"
				}, 400

			if len(users) == 0:
				# if the number of users solved is empty, then add a special first blood solve
				db.addSolve(challengeName, username, True)

			else:
				# otherwise, add a normal solve
				db.addSolve(challengeName, username, False)

			return {
				"message": "Correct!"
			}, 200

		# Incorrect
		else:
			return {
				"message": "Incorrect :("
			}, 400