"""Flask Login With Sqlalchemy"""
from flask import Flask, url_for, render_template, request, redirect, session
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper

app = Flask(__name__)

engine = create_engine('mysql+pymysql://root:@localhost/py_useradministration')
metadata = MetaData()
connection = engine.connect()
metadata.reflect(bind=engine)
users = metadata.tables['users']
Session = sessionmaker(bind=engine)
session = Session()

# data = session.query(User).filter_by(username=name, password=passw).first()
# print(data)
# exit()

class User(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password

mapper(User, users)

@app.route('/', methods=['GET', 'POST'])
def home():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		# request.method == 'POST'
		name = request.form['username']
		passw = request.form['password']
		try:
			mapper(User, users)
			data = session.query(User).filter_by(username=name, password=passw).first()
			if data is not None:
				session['logged_in'] = True
				return redirect(url_for('home'))
			else:
				return 'Dont Login 1'
		except:
			return "Dont Login 2"

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		mapper(User, users)
		new_user = User(request.form['username'], request.form['password'])
		session.add(new_user)
		session.commit()
		return render_template('login.html')
	return render_template('register.html')

@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.debug = True
	app.run(host='127.0.0.1')
	