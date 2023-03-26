# /api.py
# Routing for the backend API

from flask import Blueprint
# from db import db # for database operations
# from utils import * # for general utiltiies
# from datetime import datetime # for login streak
# from middlewares import * # for login auth
# import json # for parsing user stats
# import zipfile # for extracting challenge files
# import shutil # for removing directories
# from challenges import stopChallenge, runningChallenges
# import os # for making directories in admin utils

api = Blueprint(
	"api", # the name, which will just be api
	__name__, # the import name, which will just be api
	url_prefix = "/api" # way to access these routes will be via /api/...
)

# Add all the routes

from .api_challenge import wrap_challenge
from .api_course import wrap_course
from .api_user import wrap_user
from .api_scoreboard import wrap_scoreboard

for wrapper in wrap_challenge, wrap_course, wrap_user, wrap_scoreboard:
	wrapper(api)