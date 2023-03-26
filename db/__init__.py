"""
Creates the CustomDatabase object that is used for database options and extends it with custom database operations from all the other modules in this directory.
"""

import sqlite3

# Custom database methods
from .db_challenge import Challenge
from .db_course import Course
from .db_user import User

class CustomDatabase: # Custom class to implement custom methods on the database object for easier querying

	"""
	Constructor for the db class. Takes in an the name of the database file.
	"""
	def __init__(self, dbFile) -> None:
		self._dbFile = dbFile # remember the database file

	"""
	Query the SQLite database.
	"""
	def query(self, query, args = [], one = False):
		conn = sqlite3.connect(self._dbFile) # sqlite3 connection to the database

		def row_factory(cursor, row):
				d = {}
				for i, col in enumerate(cursor.description):
					d[col[0]] = row[i] # Iterate through the fetched values, and for each value, add the value to the corresponding column (key) in the dictionary
				return d

		conn.row_factory = row_factory # defining a better format to return the results in, for better fetching

		cursor = conn.cursor() # get a cursor to execute queries on
		cursor.execute(query, args) # execute the query with the given args
		res = cursor.fetchall() # fetch the result
		conn.commit() # save changes
		conn.close() # to the database
		if one:
			if not res: return None # if no results, return None, as this will be the expected format
			return res[0] # if only one required, return only one
		else:
			if not res: return [] # if no results, return an empty list, as this will be the expected format
			return res # otherwise, return all

"""
Extend the custom database with each module's methods.
This is done by iterating through __dict__ (which contains a mapping of every attribute to its value) and setting it on CustomDatabase.
Dunder methods (double underscore) are ignored since they are automatically added by Python.
"""
for _class in Challenge, Course, User:
	for key, value in _class.__dict__.items():
		if key.startswith("__"): continue
		setattr(CustomDatabase, key, value)


# Initialise the database
_dbConn = sqlite3.connect("db.db")
_dbConn.cursor().executescript(open("init.sql").read())
_dbConn.commit()
_dbConn.close()

db = CustomDatabase("db.db")