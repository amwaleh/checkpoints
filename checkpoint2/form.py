from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email

class SignupForm(Form):
	firstname = StringField('first Name', validators=[DataRequired("add first name")])
	lastname = StringField('last Name', validators=[DataRequired("add Last Name")])
	email = StringField('Email', validators=[DataRequired("Input email")])
	password = StringField('password',validators=[DataRequired("Password Required")])
	submit = SubmitField('Signup')