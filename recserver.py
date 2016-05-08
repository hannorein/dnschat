#import xml.etree.ElementTree as ET
import glob
import os
#import oec_plots
from flask import Flask, abort, render_template, send_from_directory, request, redirect, Response, make_response

class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

app = FlaskApp(__name__)

@app.route('/')
@app.route('/index.html')
def page_planet_redirect():
	cur = """
	<html>
	<body>
	Current message reads:
	"""
	with open("/home/hanno/git/dnschat/msg.txt","r") as f:
		cur += f.read()
	cur += """
	<form method="post" action="/recv/">
	<label for="msg">Please enter new message: </label>
	<input type="text" name="msg" /><br />
	<input type="submit" />
	</form>
	</body>
	</html>
	"""
	return cur


@app.route('/recv/', methods=['POST'])
def hello():
	msg=request.form['msg']
	with open("/home/hanno/git/dnschat/msg.txt","w") as f:
		f.write(msg)
	return "Saved. Message is now: %s<br/><br/>"%msg


if __name__ == '__main__':
    app.run(debug=True,threaded=True)
