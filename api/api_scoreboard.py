from db import db
from flask import jsonify

def wrap_scoreboard(api):

	@api.route("/scoreboard")
	def scoreboard():
		"""
		API GET to view the scoreboard, a sorted JSON array of objects of key-value pairs of username and totalPoints, sorted by point count descending.
		"""
		allUserPoints = db.getAllUserPoints() # totalPoints of all the users on the platform

		# allUserPoints is an unsorted list of dictionaries of username and totalPoints. Sort by totalPoints.
		allUserPoints = sorted(allUserPoints, key = lambda d: d["totalPoints"], reverse = True)

		return jsonify(allUserPoints), 200