import random
import json

# read in all of the names from the files
firstNames = open("firstnames.txt").readlines()
surnames = open("surnames.txt").readlines()

# a list of random actions
actions = [
	"Connected to the network.",
	"Disconnected from the network.",
	"Logged in.",
	"Logged out.",
	"Accessed a file.",
	"Deleted a file.",
	"Renamed a file."
]

dump = []
for i in range(1000):

	# generate 1000 pieces of random data
	data = {}
	data["firstName"] = random.choice(firstNames)
	data["surname"] = random.choice(surnames)
	data["logs"] = random.chocie(actions)
	dump.append(data)

# write it to the data dump file
open("./html/data.json", "w").write(
	json.dumps(dump)
)