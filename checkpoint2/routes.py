from flask import jsonify, Flask, render_template, request, session, redirect, url_for
from models import db ,users, Bucketlist, Bucketitems
from form import SignupForm, LoginForm, AddBucketlist


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://localhost/flask'
db.init_app(app)

app.secret_key = "development-Key"

@app.route("/list",methods=["GET","POST"])
def bucketlist():
	form = AddBucketlist()
	if request.method == 'POST':
		if form.validate() == False:

			return render_template("index.html",form=form)
		else:
			newlist = Bucketlist(
								 form.name.data
								 )
			db.session.add(newlist)
								 
			db.session.commit()
			return request.data
	if request.method == 'GET':
		lists = db.session.query(Bucketlist).all()
		
		return jsonify(Bucketlist=[i.serialize for i in db.session.query(Bucketlist).all()])


#index page route index.html
@app.route("/")
def index():
	return render_template("index.html")

# route to about page about.html
@app.route("/about")
def about():
	return render_template("about.html")

# Route to Sign up page 
@app.route("/signup",methods=["GET","POST"])
def signup():
	# generate Signupform from form.py
	form = SignupForm()
	# Check if the form has been submitted 
	if request.method == 'POST':
		# validate the form 
		if form.validate() == False:
			# if form fails redirect back signup form
			return render_template('signup.html',form=form)
		else:
			# if form passes take the submited request and  save user details 
			
			newuser = users(form.firstname.data,
						   form.lastname.data,
						   form.email.data,
						   form.password.data)
			db.session.add(newuser)
			db.session.commit()
			
			# Return message 
			return "user Created"#render_template('index.html', content={'msg':'welcome you are'})
	# Else check if its first form request
	elif request.method == 'GET' :
		return render_template('signup.html', form=form)

# Route to Login Page 
@app.route("/login", methods=["GET","POST"])
def login():
	# generate form from form.py template
	form = LoginForm()
	#check if form has been submited 
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('login.html', form=form)

		else:

			#check for email
			email = form.email.data 
			password = form.password.data
			user = users.query.filter_by(email=email).first()
			if user is not None and user.check_password(password):
				return redirect(url_for("index"))
			#if Fail return to Login 
			#if pass redirect to home page 
			else:
				return render_template('login.html', form=form)

	if request.method == 'GET':
		return render_template('login.html', form=form)



if __name__ == "__main__" :
	app.run(debug=True)