from flask import *
import sys
import socket
from urllib.parse import urlparse

app = Flask(__name__)

def constructRequest(url, headers):
	if "flag" in url.path: raise ValueError("Destination not allowed")

	request = f"""\
		GET {url.path or "/"} HTTP/1.1\r
	""".replace("\t", "")

	# add headers
	for header in headers:
		key, value = header

		# to avoid 400 errors, change the host to the proxied URL
		if key == "Host": value = url.hostname

		request += f"{key}: {value}\r\n"

	# to denote the end of the request, another "\r\n" is needed
	# otherwise it's ambiguous to the server as it could mean that another header is coming, but the client is just slow
	request += "\r\n"
	return request

def sendRequest(request, dest_socket):

	# create the connection to the server, send, and read
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(dest_socket)
		s.sendall(bytes(request, "utf-8"))

		data = s.recv(1024)

	return data

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/flag")
def flag():
	if request.remote_addr != "127.0.0.1": return "Not allowed"
	elif request.headers.get("X-Flag-Ask-Nicely") != "please": return "Not with that attitude"
	else: return "Because you asked so nicely: ctf{http_de1ty}"

@app.route("/proxy")
def proxy():

	url = urlparse(request.args.get("url"))

	try:
		raw_request = constructRequest(url, request.headers)
	except e:
		return render_template("index.html", error = e)

	dest_socket = (url.hostname, url.port or 80)

	try:
		data = sendRequest(raw_request, dest_socket).decode("latin-1")
	except e:
		return render_template("index.html", error = e)

	return render_template("result.html", data = data)


if len(sys.argv) == 2: app.run("0.0.0.0", sys.argv[1])
else: app.run("0.0.0.0", 3000)