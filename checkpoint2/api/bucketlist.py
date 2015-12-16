from flask import json,jsonify, session, Flask, session, \
					escape, render_template, request,\
					session, redirect, url_for,g
from models import db, users, Bucketlist, Bucketitems
from form import SignupForm, LoginForm, AddBucketlist
from flask.ext.httpauth import HTTPBasicAuth
from sqlalchemy_paginator import Paginator
from flask.ext.sqlalchemy  import Pagination
from config import POSTS_PER_PAGE
from flask import Blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask'
app.config['SECRET_KEY'] = "development-Key"
#app.config["JSON_SORT_KEYS"] = False
db.init_app(app)
auth = HTTPBasicAuth()
mod = Blueprint('users', __name__)

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
		post_per_page = POSTS_PER_PAGE
		limit = request.args.get('limit')
		q_name = request.args.get('q')
		if limit:
			if  int(limit) > 0 and int(limit) <= 100 :
				post_per_page = int(limit)
			# Set maximum number of pages
			if int(limit) > 100:
				post_per_page = 100

		query = db.session.query(Bucketlist).filter_by(creator=uid)

		if q_name:
			query = db.session.query(Bucketlist).filter_by(creator=uid).filter_by(name=q_name)


		pagination = Paginator(query,post_per_page)
		page=1
		current_page = pagination.page(page)
		lists = current_page.object_list
		if lists == []:
			return jsonify({'Error':'Bucketlist Empty'})
		all_lists = [List.serialize for List in lists]

		next_page = None
		previous_page = None

		if current_page.has_next():
			next_page = current_page.next_page_number
		if current_page.has_previous():
			previous_page = current_page.has_previous()


		pages_view = {
                    'total_count': current_page.paginator.count,
                    'total_pages': current_page.paginator.total_pages,
                    'current_page': current_page.number,
                    'next_page': next_page,
                    'previous_page': previous_page,
                    'bucketlists': all_lists
                 }
		return jsonify(Bucketlist=[pages_view])


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
		username = request.args.get('username')
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
		items=[i.serializeitem for i in 
						   db.session.query(Bucketitems).
						   filter(
									Bucketlist.creator == uid, 
									Bucketlist.id == id,
									Bucketitems.id == item_id
									)]
		if len(item) == 0 :
			return jsonify({'Error':'No Item Found'})
		return jsonify(items=items)
		

# index page route index.html
@mod.route('/')
@app.route("/")
@auth.login_required
def index():
	uid = "%d"%g.user.uid
	query = db.session.query(Bucketlist).filter_by(creator=uid)
	pagination = Paginator(query,POSTS_PER_PAGE)
	page=1
	current_page = pagination.page(page)
	bucketlists = current_page.object_list
	#users = User.find(...)
	#pagination = Pagination(page=page, total=count, search=count, record_name='users')
	return jsonify(Bucketlist=[lists.serialize for lists in bucketlists])


# route to about page about.html
@app.route("/about")
@auth.login_required
def about():
	return render_template("about.html")

# Route to Sign up page

@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201,\
    				{'Location': url_for('get_user', 
    									  id = user.id, 
    									  _external = True
    									)
    				}
	

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

@app.route("/auth/logout")
def logout():
	g.user=""
	return str(g.user)#jsonify({"Message":"You Been Logged Out"})

if __name__ == "__main__" :
	app.run(debug=True)