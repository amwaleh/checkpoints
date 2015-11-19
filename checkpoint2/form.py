from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired

class SignupForm(Form):
	first_name = StringField('first Name', validators=[DataRequired()])
	last_name = StringField('last Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	submit = SubmitField('Signup')