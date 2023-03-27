# /middlewares.py
# Route protection (i.e login protection, etc.)

from flask import *
from db import db # for database operations
import functools # so can be used as a decorator

"""
Decorator to reject a request if the user is unauthenticated. For the frontend.
"""
def webLoginRequired(fn):
	@functools.wraps(fn) # decorates the route
	def wrapper(*args, **kwargs):
		if "username" not in session:
			return redirect(url_for("web.login")) # send them to the login page
		return fn(*args, **kwargs) # otherwise, simply continue
	return wrapper

"""
Decorator to reject a request if the user is unauthenticated. For the backend API, so a JSON error message is given.
"""
def apiLoginRequired(fn):
	@functools.wraps(fn) # decorates the route
	def wrapper(*args, **kwargs):
		if "username" not in session:
			return {
				"message": "You are not logged in!"
			}, 403
		return fn(*args, **kwargs) # otherwise, simply continue
	return wrapper