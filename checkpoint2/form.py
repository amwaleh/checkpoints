from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email

class SignupForm(Form):
	firstname = StringField('first Name', validators=[DataRequired("add first name")])
	lastname = StringField('last Name', validators=[DataRequired("add Last Name")])
	email = StringField('Email', validators=[DataRequired("Input email")])
	password = PasswordField('password',validators=[DataRequired("Password Required")])
	submit = SubmitField('Signup')

class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired("Input email")])
	password = PasswordField('password',validators=[DataRequired("Password Required")])
	submit = SubmitField('Login')

class AddBucketlist(Form):
	name = StringField('List', validators=[DataRequired("add list")])
	submit = SubmitField('add list')