# /app.py

from flask import * # imports Flask, which is the web microframework I will be using
from db import db # imports the database for database operations
from challenges import (
	init as init_challenges # for starting challenges
)

# Blueprints
from api import api
from web import web

app = Flask(__name__) # instantiate the app
app.register_blueprint(api) # register blueprints
app.register_blueprint(web) # ...

app.config.from_object("config.DevelopmentConfig") # load the config from my config file, in order to keep all the config in one place neatlychallengeName

init_challenges() # start challenges

app.run("0.0.0.0", 2001) # run the app