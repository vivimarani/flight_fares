from flask import Flask
from flask import render_template
from os import path

'''
export FLASK_APP=app.py
flask run
'''

d = path.dirname(__file__)
app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def index():
	# query = """SELECT * FROM trips LIMIT 20"""
	return render_template('index.html')
