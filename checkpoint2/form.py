from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email

class SignupForm(Form):
	first_name = StringField('first Name', validators=[DataRequired("add first name")])
	last_name = StringField('last Name', validators=[DataRequired("add Last Name")])
	email = StringField('Email', validators=[DataRequired("Input email"),Email])
	submit = SubmitField('Signup')