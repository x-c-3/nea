"""
Defines database operations to do with courses.
"""

class Course:
	"""
	Fetch all information about a course by name.
	"""
	def getCourseInfo(self, courseName):
		res = self.query("SELECT * FROM Course WHERE courseName = ?", [
			courseName
		], one = True)
		return res

	"""
	Fetch all information about all courses.
	"""
	def getCourseInfos(self):
		res = self.query("SELECT * FROM Course")
		return res

	"""
	Fetch the names of all courses.
	"""
	def getCourseNames(self):
		res = self.query("SELECT courseName FROM Course")
		# list comprehension to convert dict to a simple list of course names, for example:
		# [{"username": 1}, {"username": 2}, {"username": 3}] becomes [1, 2, 3]
		res = [d.get("courseName") for d in res]
		return res

	"""
	Fetch all the levels in a course.
	"""
	def getLevelsInCourse(self, courseName):
		res = self.query("SELECT levelNo, infos FROM Level WHERE courseName = ?", [
			courseName
		])
		return res

	"""
	Fetch the names of all the challenges in a course.
	"""
	def getChallengesInCourse(self, courseName):
		res = self.query("SELECT challengeName FROM Challenge WHERE courseName = ?", [
			courseName
		])
		# list comprehension to flatten to a list
		res = [d.get("challengeName") for d in res]
		return res

	"""
	Fetch the names of all the challenges in a level.
	"""
	def getChallengesInLevel(self, courseName, levelNo):
		res = self.query("SELECT challengeName FROM Challenge WHERE courseName = ? AND levelNo = ?", [
			courseName,
			levelNo
		])
		# list comprehension to flatten to a list
		res = [d.get("challengeName") for d in res]
		return res

	"""
	Add a user solve to a course.
	"""
	def addCourseSolve(self, courseName, username):
		self.query("INSERT INTO CourseSolve (courseName, username) VALUES (?, ?)", [
			courseName,
			usernam
		])
		return

	"""
	Get the users who have solved a course.
	"""
	def getCourseSolves(self, courseName):
		self.query("SELECT username FROM CourseSolve WHERE courseName = ?", [
			courseName
		])
		return