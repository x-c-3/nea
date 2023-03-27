from flask import *
import sys
import random

app = Flask(__name__)

impossible_questions = {
	"What number am I thinking of?": "3769285254890",
	"What colour is the pencil?": "Turquoise",
	"What's my favourite colour?": "Viridian",
	"What is the first prime that is even and a square number?": "My guess is as good as yours",
	"What is the first number that is both odd and even?": "Who knows",
	"Can you answer this question?": "Yes I can, this answer is correct",
	"?yas siht seod tahW": "The correct answer"
}

@app.route("/")
def process_answer():

	num_correct = int(request.cookies.get("num_correct", 0))
	current_question = request.cookies.get("current_question")
	user_answer = request.args.get("answer")

	if num_correct >= 1000: return render_template("index.html", flag = "ctf{c00kie_monster}")

	real_answer = impossible_questions.get(current_question)

	# first time arriving
	# set the user a random question and initialise num_correct
	if not current_question:

		new_question = random.choice(list(impossible_questions.keys()))
		resp = make_response(render_template("index.html", question = new_question, num_correct = num_correct))
		resp.set_cookie("current_question", new_question)
		resp.set_cookie("num_correct", "0")

		return resp

	# no answer given
	# render the normal page
	if not user_answer: return render_template("index.html", question = current_question, num_correct = num_correct)

	# incorrect answer
	if real_answer != user_answer:
		return render_template("index.html", msg = "Incorrect answer, try again!", num_correct = num_correct, question = current_question)

	# correct answer
	elif real_answer == user_answer:

		# generate a new question and set cookies
		new_question = random.choice(list(impossible_questions.keys()))
		new_num_correct = num_correct + 1
		resp = make_response(render_template("index.html", msg = "Correct!", question = new_question, num_correct = new_num_correct))
		resp.set_cookie("current_question", new_question)
		resp.set_cookie("num_correct", str(new_num_correct))

		return resp

if len(sys.argv) == 2: app.run("0.0.0.0", sys.argv[1])
else: app.run("0.0.0.0", 3000)