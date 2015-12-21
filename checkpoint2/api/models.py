
from config import SECRET
from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.appbuilder import ModelView
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


SECRET_KEY = SECRET
db = SQLAlchemy()

class Users(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120))
	logged = db.Column(db.Boolean)
	pwdhash = db.Column(db.String(255))
	created_on = db.Column(db.DateTime, server_default=db.func.now())
	modified_on = db.Column(db.DateTime, server_default=db.func.now(),
		                                 onupdate=db.func.now())

	def __init__(self,username,firstname=None, lastname=None, email=None, logged=False):
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.username = username
		self.logged = logged

	def hash_password(self, password):
		self.pwdhash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.pwdhash)
	
	def generate_auth_token(self, expiration=600):
		s = Serializer(SECRET_KEY, expires_in=expiration)
		data = {'username': self.username} if self.username is not None else {}
		return s.dumps({'uid': self.uid})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(SECRET_KEY)
		try:
			data = s.loads(token)
			user =Users.query.filter_by(uid=data['uid']).first()
		except SignatureExpired:
			return None
		except BadSignature :
			return None
			
		user =Users.query.get(data['uid'])
		return user

class Bucketitems(db.Model):
	__tablename__ ='bucketitem'
	id = db.Column(db.Integer,primary_key=True)
	list =db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
	name = db.Column(db.String(100))
	done = db.Column(db.Boolean)
	created_on = db.Column(db.DateTime, server_default=db.func.now())
	modified_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

	def __init__(self, name,list, id=None, created_on=None, modified_on=None,done=False):
		self.name = name
		self.id = id 
		self.list = list
		self.done = done
		self.created_on = created_on
		self.modified_on = modified_on

	def __repr___(self):
		 return '<name %r>' % (self.name)

	@property
	def serialize(self):
		''' serialize output of bucketlist '''
		return {
				'id': self.id,
				'name': self.name,
				'done': self.done,
				'date_created': self.created_on,
				'date_modified': self.modified_on
				}
	@property
	def serializeitem (self):
		''' Serialize items from Bucketitems '''
		return {
				'name': self.name,
				'done': self.done
				}

	@property
	def serialize_many2many(self):
		''' Serialize items in the relationship object '''
		return  [ list.serialize for list in self.list]

class Bucketlist(db.Model):
	__tablename__ ='bucketlist'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	item = db.relationship('Bucketitems', backref='items', lazy='dynamic')
	creator = db.Column(db.Integer, db.ForeignKey('users.uid'))
	created_on = db.Column(db.DateTime, server_default=db.func.now())
	modified_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
	
		
	def __init__(self,name,creator=None,id=None,created_on=None,modified_on=None,item={}):
		self.id = id 
		self.item = item
		self.name = name
		self.creator = creator
		self.created_on = created_on
		self.modified_on = modified_on

	# Function to serialize the data that will be retrieved 
	@property
	def serializelist(self):
	    return {
				'id': self.id,
				'name': self.name,
				'created_on': self.created_on,
				'modified_on': self.modified_on
				}

	@property
	def serialize (self):
		return {
				'id': self.id,
				'name': self.name,
				'items': self.serialize_many2many,
				'created_on': self.created_on,
				'modified_on': self.modified_on,
				'created_by': self.creator
				}
	@property
	def serializeitem (self):
		return {'items': self.serialize_many2many}

	# Function to Serialize the realtionship
	@property
	def serialize_many2many(self):
	    return  [ item.serialize for item in self.item]


	def __repr__(self):
		 return "{0}".format(self.name)	
