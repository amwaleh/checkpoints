from flask import json,jsonify, session, Flask, session, escape, render_template, request, session, redirect, url_for,g
from models import db, users, Bucketlist, Bucketitems
from form import SignupForm, LoginForm, AddBucketlist
from flask.ext.httpauth import HTTPBasicAuth
import ast

app = Flask(__name__)
app.make_config["JSON_SORT_KEY"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask'
db.init_app(app)

app.config['SECRET_KEY'] = "development-Key"

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = users.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = users.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route("/api/token")
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({ 'token': token.decode('ascii') })


@app.route("/bucketlists", methods=["GET", "POST"])
@auth.login_required
def bucketlist():
	uid = "%d"%g.user.uid
	if request.method == 'POST':
		data = request.get_json(force=True)
		name = request.json.get('name',)
		# check if the name was set
		if name is None:
			return 'render_template("index.html",form=form)'
		else:
			# Save the List and start a session for the list
			newlist = Bucketlist(name,uid)
			db.session.add(newlist)
			db.session.flush()
			session['bucketlist'] = newlist.id
			db.session.commit()
			return jsonify({"id": newlist.id})

	if request.method == 'GET':
		uid = "%d"%g.user.uid
		
		return jsonify(Bucketlist=[ i.serializelist for i in 
					   db.session.query(Bucketlist).filter_by
					   (creator=uid)])

@app.route("/bucketlists/<int:id>", methods=["GET", "PUT"])
@auth.login_required
def Update_bucketlist(id):
	uid = "%d"%g.user.uid
	if request.method == 'PUT':
		data = request.get_json(force=True)
		name = request.json.get('name',)
		# check if the name was set
		if name is None:
			return 'render_template("index.html",form=form)'
		else:
			# Save the List and start a session for the list
			newlist = Bucketlist.query.get(id)
			newlist.name = name			
			db.session.commit()
			return jsonify(Bucketlist=[ i for i in 
					   db.session.query(Bucketlist.name).filter_by
					   (creator=uid, id=id)])
	if request.method == 'GET':
		uid = "%d"%g.user.uid
		
		return jsonify(Bucketlist=[ i for i in 
					   db.session.query(Bucketlist.name,Bucketlist.id).filter_by
					   (creator=uid, id=id)])

# Endpoint for adding Items
@app.route("/bucketlists/<int:id>/items", methods=["GET", "POST"])
@auth.login_required
def bucketitems(id):
	print("Add Items")
	uid = "%d"%g.user.uid
	if request.method == 'POST':
		data = request.get_json(force=True)
		item = request.json.get('name')
		if item is None :
			return jsonify({'Error':'Bucketitem Name is required'})
		
		newitem = Bucketitems(item,id)
		db.session.add(newitem)
		db.session.flush()
		db.session.commit()
		return jsonify(Bucketlist=[i.serialize for i in 
						db.session.query(Bucketlist).filter_by
						(creator=int(uid))])
	
	if request.method == 'GET':
		result = jsonify(Bucketlist=[i.serialize for i in 
						   db.session.query(Bucketlist).filter_by
						   (id=id,creator=int(uid))])
		return result


# index page route index.html
@app.route("/")
@auth.login_required
def index():
	return "Hello, %s" % g.user.uid

# route to about page about.html
@app.route("/about")
@auth.login_required
def about():
	return render_template("about.html")

# Route to Sign up page
@app.route("/signup", methods=["POST"])
def signup():
	""" Get data in JSON format"""
	data = request.get_json(force=True)
	# Get username and password  to register user
	username = request.json.get('username')
	password = request.json.get('password')
	# Check if User and password have been passed
	if username is None or password is None:
		return jsonify({'Error':'Username and password required'})
	# Check if user exist in the database 
	if users.query.filter_by(username = username).first() is not None:
		return jsonify({'Error':'User exists'})
	# Save newuser 
	user = users(username = username)
	user.hash_password(password)
	user.firstname = request.json.get('firstname')
	user.lastname = request.json.get('lastname')
	user.email = request.json.get('email')
	db.session.add(user)
	db.session.commit()
	return jsonify({ 'username': user.username })
	

# Route to Login Page 
@app.route("/auth/login", methods=["GET","POST"])
def login():
	# generate form from form.py template
	form = LoginForm()
	# check if form has been submited 
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('login.html', form=form)		
		# check for email
		email = form.email.data 
		password = form.password.data
		user = users.query.filter_by(email=email).first()
		if user is not None and user.check_password(password):
			return redirect(url_for("index"))

		'''	if all Fail return to Login 
			if pass redirect to home page '''		
		return render_template('login.html', form=form)

	if request.method == 'GET':
		return render_template('login.html', form=form)



if __name__ == "__main__" :
	app.run(debug=True)
