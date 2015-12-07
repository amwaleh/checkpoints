import routes
from flask import json,jsonify, session, Flask, session, \
					escape, render_template, request,\
					session, redirect, url_for,g
from models import db, users, Bucketlist, Bucketitems
from form import SignupForm, LoginForm, AddBucketlist
from flask.ext.httpauth import HTTPBasicAuth
from sqlalchemy import and_
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

# *Endpoint for listing all bucketlist of a user
@app.route("/bucketlists", methods=["GET", "POST"])
@auth.login_required
def bucketlist():
	uid = "%d"%g.user.uid
	if request.method == 'POST':
		data = request.get_json(force=True)
		name = request.json.get('name',)
		# check if the name was set
		if name is None:
			return jsonify({'Error':'List Name required'})
		# Save the List and start a session for the list
		newlist = Bucketlist(name,uid)
		db.session.add(newlist)
		db.session.flush()
		#Create session for adding Items
		session['bucketlist'] = newlist.id
		db.session.commit()
		return redirect(("/bucketlists/{0}".format(newlist.id)))

	if request.method == 'GET':
		newList = db.session.query(Bucketlist).filter(Bucketlist.creator == uid)
		# Serialise items and create item
		Lists = [List.serializelist for List in newList]
		# Check if the list is Empty
		if len(Lists) == 0 :
			return jsonify({'Error':'Empty'})
		return jsonify(Bucketlist = Lists)

@app.route("/bucketlists/<int:id>", methods=["GET", "PUT", "DELETE"])
@auth.login_required
def Update_bucketlist(id):
	uid = "%d"%g.user.uid
	if request.method == 'PUT':
		data = request.get_json(force=True)
		name = request.json.get('name',)
		# check if the name was set
		if name is None:
			return 'name Field Required'
		# Save the List and start a session for the list
		newlist = Bucketlist.query.get(id)
		if newlist is None:
			return jsonify({'Error':'List does not Exist'})
		newlist.name = name			
		db.session.commit()
		lists =db.session.query(Bucketlist.name).\
				   filter(Bucketlist.creator == uid,
				   		  Bucketlist.id == id
				   		  )
		return jsonify(Bucketlist=[list for list in lists])

	if request.method == "DELETE":
		del_list = Bucketlist.query.get(id)
		# If ID does not exist Exit
		if del_list is None :
			return "List does not exist"
		# Else delete and update the database
		db.session.delete(del_list)
		db.session.commit()
		return jsonify({"error":"List deleted"})

	if request.method == 'GET':
		uid = "%d"%g.user.uid
		#Check if list exists 
		newList = Bucketlist.query.get(id)
		if newList is None:
			return jsonify({'Error':'List does not Exist'})

		newList = db.session.query(Bucketlist.name,Bucketlist.id).\
				   				filter(
				   					    Bucketlist.creator == uid, 
				   					    Bucketlist.id ==id
				   					    )
		return jsonify(Bucketlist=[list for list in newList])

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
		items = db.session.query(Bucketlist).filter\
						  (Bucketlist.creator == uid)

		return jsonify(Bucketlist=[item.serialize for item in items])
	
	if request.method == 'GET':
		items = db.session.query(Bucketlist).\
				filter(
			   		    Bucketlist.creator == uid,
			   		    Bucketlist.id == id
			   		   )

		return jsonify(Bucketlist=[item.serialize for item in items])
		

@app.route("/bucketlists/<int:id>/items/<int:item_id>", methods=["GET", "PUT", 'DELETE'])
@auth.login_required
def update_items(id, item_id):
	
	uid = "%d"%g.user.uid
	if request.method == 'PUT':
		data = request.get_json(force=True)
		item = request.json.get('name')
		if item is None :
			return jsonify({'Error':'Bucketitem Name is required'})
		
		newitem = Bucketitems.query.get(item_id)
		if newitem is None:
			return "Item does not exist"
		newitem.name = item
		db.session.commit()
		return jsonify(items=[i.serializeitem for i in 
						   db.session.query(Bucketitems).
						   filter(
									Bucketlist.creator == uid, 
									Bucketlist.id == id,
									Bucketitems.id == item_id
									)])

	if request.method == 'DELETE':
		del_item = Bucketitems.query.get(item_id)
		# if Item does not exist escape
		if del_item is None:
			return "List does not exist"
		# Else Delete Item and commit
		db.session.delete(del_item)
		db.session.commit()
		return "item Deleted"
	
	if request.method == 'GET':
		return jsonify(items=[i.serializeitem for i in 
						   db.session.query(Bucketitems).
						   filter(
									Bucketlist.creator == uid, 
									Bucketlist.id == id,
									Bucketitems.id == item_id
									)])
		

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
@app.route("/signup", methods=["POST",'GET'])
def signup():
	""" Get data in JSON format"""
	data = request.get_json(force=True)
	# Get username and password  to register user
	username = request.json1.get('username')
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