from flask.ext.sqlalchemy import SQLAlchemy
#from wezeug import


db = SQLAlchemy()

class user(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer,primary_key =True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	password =db.column(db.password(120))

	def __init__ (self, firstname, lastname,email):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
