# /challenges.py
# Utils for handling challenges

from flask import *
import random # to get a random port
import subprocess # to run the flask command
import atexit # for the exit hook
from db import db # to get all challenges
import os

runningChallenges = [] # A list of all the currently running challenges
homeDir = os.getcwd() # home directory as a reference

"""
Start a challenge, identified by name, and host it at /play/:challengeName.
Challenge files must be in /challenges/:challengeName/.

There must be an app.py in the challenge folder root. This will be run in the format:

$ python3 path/to/app.py port

Example code to add to the end:

# Run the below code to start the challenge
if __name__ == '__main__':
	import sys
	port = sys.argv[1]
	app.run("127.0.0.1", port)
"""
def startChallenge(challengeName):
	randomPort = str(random.randint(10000, 11000))
	runningChallenges.append({
		"challengeName": challengeName,
		"process": subprocess.Popen(["python3", "app.py", randomPort], cwd=f"{homeDir}/challenges/{challengeName}"), # run the challenge
		"port": randomPort # the port
	})

"""
Stop all challenges.
"""
def stopAllChallenges():
	for processData in runningChallenges: processData["process"].terminate()

"""
Stop a specific challenge.
"""
def stopChallenge(challengeName):
	for processData in runningChallenges:
		if processData["challengeName"] == challengeName:
			processData["process"].terminate()


def init():
	atexit.register(stopAllChallenges) # run on exit

	for challengeName in db.getChallengeNames():
		startChallenge(challengeName)