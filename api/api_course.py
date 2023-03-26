from db import db
from middlewares import *
import json

def wrap_course(api):

	@api.route("/course/<courseName>")
	@apiLoginRequired
	def getCourse(courseName):
		"""
		Frontend interface to get course info.
		Course info includes:
			- challenges (array of challenge names)
			- courseName
			- shortDesc
			- levels (array of objects):
				- levelNo
				- infos
				- challenges (array of challenge names in that level)
		---
		parameters:
			-	name: courseName
				in: path
				type: string
				required: true
				description: Name of the course
		"""
		info = db.getCourseInfo(courseName)
		if info == None: return {
			"message": "Course does not exist"
		}, 400

		# add all the challenges
		containedChallenges = db.getChallengesInCourse(courseName)
		info["challenges"] = containedChallenges

		# add all the levels
		containedLevels = db.getLevelsInCourse(courseName)

		# add all the contained challenges in each level, and parse the infos from JSON
		for level in containedLevels:
			challenges = db.getChallengesInLevel(courseName, level.get("levelNo"))
			level["challenges"] = challenges
			level["infos"] = json.loads(level["infos"])

		info["levels"] = containedLevels

		return info, 200

	@api.route("/courses")
	@apiLoginRequired
	def getCourses():
		"""
		Frontend interface to get all course names. If no username is given, return all course names.
		---
		parameters:
			-	name: username
				in: query
				type: str
				required: true
				description: User to get all the solved courses of.
			-	name: infos
				in: query
				type: str
				description: If given, return all infos instead
		"""
		username = request.args.get("username", "")
		infos = request.args.get("infos")

		# if username given, give all the course names that user has solved
		if username:
			res = db.getSolvedCourseNames(username)
			return jsonify(res), 200

		# if infos given, return infos instead
		if infos:

			courseInfos = db.getCourseInfos()

			for courseInfo in courseInfos:
				courseName = courseInfo["courseName"]

				# add all the challenges
				containedChallenges = db.getChallengesInCourse(courseName)
				courseInfo["challenges"] = containedChallenges

				# add all the levels
				containedLevels = db.getLevelsInCourse(courseName)

				# add all the contained challenges in each level, and parse the infos from JSON
				for level in containedLevels:
					challenges = db.getChallengesInLevel(courseName, level.get("levelNo"))
					level["challenges"] = challenges
					level["infos"] = json.loads(level["infos"])

				courseInfo["levels"] = containedLevels

			return jsonify(courseInfos), 200

		# otherwise, just return all challenges
		else:
			return jsonify(db.getCourseNames()), 200

	@api.route("/course/<courseName>/solve", methods = ["POST"])
	@apiLoginRequired
	def solveCourse(courseName):
		"""
		Solve a course if all the challenges have been completed.
		---
		parameters:
			-	name: courseName
				in: path
				type: string
				required: true
				description: Name of the course
		"""
		courseData = db.getCourseInfo(courseName) # data about the course
		if courseData == None: return {
			"message": "Course does not exist!"
		}, 400
		points = courseData.get("points")
		username = session["username"]

		# Logic to check that they have solved all the challenges in the course
		containedChallenges = db.getChallengesInCourse(courseName)
		for challengeName in containedChallenges:
			challengeSolves = db.getSolves(challengeName) # Get the users who have solved the challenge
			if username not in challengeSolves: # haven't solved this challenge
				return {
					"message": "You haven't completed every challenge!"
				}, 400

		# Logic to check that they have not already solved the course

		# Get all users who solved the course
		users = db.getCourseSolves(courseName)

		# if the user does exist, they have already solved, so do nothing
		if username in users:
			return {
				"message": "You have solved this course already!"
			}, 400

		# otherwise, add a solve
		db.addCourseSolve(courseName, username)

		return {
			"message": "Solved!"
		}, 200