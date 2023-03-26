# /config.py

import os

class Config(object):
	SECRET_KEY = os.urandom(32) # securely generated random secret key
	TEMPLATES_AUTO_RELOAD = True # reload templates during development to reduce times needed to reload app to reflect changes

class ProductionConfig(Config):
	pass # to be added

class DevelopmentConfig(Config):
	DEVELOPMENT = True # flag to tell Flask that I am in development
	# DEBUG = True # for local debugging
	HOST = "127.0.0.1" # localhost testing