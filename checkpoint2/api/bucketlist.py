from flask import json, jsonify, session, Flask, session, \
    			  escape, render_template, request,\
   				  session, redirect, url_for, g
from models import db, Users, Bucketlist, Bucketitems
from form import SignupForm, LoginForm, AddBucketlist
from flask.ext.httpauth import HTTPBasicAuth
from sqlalchemy_paginator import Paginator
from config import POSTS_PER_PAGE, MAX_PAGES, DATABASE_URI, SECRET
from flask.ext.login import (current_user, LoginManager, login_user,
                             logout_user, login_required)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = "development-Key"
app.config["JSON_SORT_KEYS"] = False
db.init_app(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    '''Checks if token is valid '''
    if 'token' in request.headers:
        token = request.headers['token']
        user = Users.verify_auth_token(token)
        if user:
            if user.logged == True:
                g.user = user
                return True
        else:
            return False


@app.route("/api/token")
@auth.login_required
def get_auth_token():
    ''' Generates Token '''
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route("/bucketlists", methods = ["GET", "POST"])
@auth.login_required
def bucketlist():
    ''' creates and listing bucketlists'''
    uid = g.user.uid
    if request.method == 'POST':
        data = request.get_json(force = True)
        name = request.json.get('name',)
        # check if the name was set
        if name is None:
            return jsonify({'Error': 'List Name required'}), 401
        # Save the List and start a session for the list
        newlist = Bucketlist(name, uid)
        db.session.add(newlist)
        db.session.flush()
        # Create session for adding Items
        session['bucketlist'] = newlist.id
        db.session.commit()
        return redirect(("/bucketlists/{0}".format(newlist.id))), 302

    if request.method == 'GET':
        post_per_page = POSTS_PER_PAGE
        limit = request.args.get('limit')
        q_name = request.args.get('q')
        page = request.args.get('page')
        ''' Check post per page '''
        if limit:
            if int(limit) > 0 and int(limit) <= 100:
                post_per_page = int(limit)
            # Set maximum number of pages
            if int(limit) > 100:
                post_per_page = 100

        ''' Set search query '''
        query = db.session.query(Bucketlist).filter_by(creator=uid)
        if q_name:
            query = db.session.query(Bucketlist).filter_by(
                creator=uid).filter_by(name=q_name)
        ''' Set page to view'''
        if not page or not page.isnumeric:
            page = 1
        pagination = Paginator(query, post_per_page)
        '''prevent out of range requests'''
        if page > str(pagination.total_pages):
            return jsonify({'Error': 'Page requested is out of Range'}), 401

        current_page = pagination.page(page)
        lists = current_page.object_list
        all_lists = [List.serialize for List in lists]
        next_page = None
        previous_page = None
        if current_page.has_next():
            next_page = current_page.next_page_number
        if current_page.has_previous():
            previous_page = current_page.has_previous()
        total_pages = str(current_page.paginator.total_pages)
        pages_view = {
            'total_count': current_page.paginator.count,
            'total_pages': current_page.paginator.total_pages,
            'current_page': current_page.number,
            'next_page': next_page,
            'previous_page': previous_page,
            'bucketlists': all_lists
        }
        return jsonify(Bucketlist = [pages_view]), 200


@app.route("/bucketlists/<int:id>", methods = ["GET", "PUT", "DELETE"])
@auth.login_required
def Update_bucketlist(id):
    ''' Update or delete bucketlist '''
    uid = g.user.uid
    if request.method == 'PUT':
    	newlist = Bucketlist.query.get(id)
        data = request.get_json(force = True)
        if 'name' in request.json:
        	newlist.name = request.json.get('name',)
      
        db.session.commit()
        lists = db.session.query(Bucketlist.name).\
            filter(
            		Bucketlist.creator == uid,
                    Bucketlist.id == id
                  )
        return jsonify(Bucketlist = [list for list in lists]), 201

    if request.method == "DELETE":
        del_list = Bucketlist.query.get(id)
        # If ID does not exist Exit
        if del_list is None:
            return "List does not exist", 404
        # Else delete and update the database
        db.session.delete(del_list)
        db.session.commit()
        return jsonify({"info": "List deleted"}), 401

    if request.method == 'GET':
        uid = g.user.uid
        # Check if list exists
        username = request.args.get('username')
        newList = Bucketlist.query.get(id)
        if newList is None:
            return jsonify({'Error': 'List does not Exist'})

        newList = db.session.query(Bucketlist.name, Bucketlist.id).\
            filter(
            		Bucketlist.creator == uid,
            		Bucketlist.id == id
        		  )
        return jsonify(Bucketlist = [list for list in newList]), 200


@app.route("/bucketlists/<int:id>/items", methods = ["GET", "POST"])
@auth.login_required
def bucketitems(id):
    ''' Add or List item to Bucketlist '''
    uid = g.user.uid
    if request.method == 'POST':
        data = request.get_json(force = True)
        item = request.json.get('name')
        if item is None:
            return jsonify({'Error': 'Bucketilist Name is required'}), 403

        newitem = Bucketitems(item, id)
        db.session.add(newitem)
        db.session.flush()
        db.session.commit()
        items = db.session.query(Bucketlist).filter(Bucketlist.creator == uid)
        return jsonify(Bucketlist = [item.serialize for item in items]), 201

    if request.method == 'GET':
        items = db.session.query(Bucketlist).\
            filter(
                    Bucketlist.creator == uid,
                    Bucketlist.id == id
                  )
        return jsonify(Bucketlist = [item.serialize for item in items]), 200


@app.route("/bucketlists/<int:id>/items/<int:item_id>", methods = ["GET", "PUT", "DELETE"])
@auth.login_required
def update_items(id, item_id):
	''' Updates items in a bucketlist '''
	uid = g.user.uid
	if request.method == 'PUT':
		newitem = Bucketitems.query.get(item_id)
		data = request.get_json(force=True)
		if  'name' in request.json:
			newitem.name = request.json.get('name')
		if 'done' in request.json:
			newitem.done = request.json.get('done')
		db.session.commit()
		return jsonify(items = [i.serializeitem for i in
		                      db.session.query(Bucketitems).
		                      filter(
		                          Bucketlist.creator == uid,
		                          Bucketlist.id == id,
		                          Bucketitems.id == item_id
		                      )]), 201

	if request.method == 'DELETE':
	    del_item = Bucketitems.query.get(item_id)
	    # if Item does not exist escape
	    if del_item is None:
	        return jsonify({'Error': 'List does not Exist'}), 404
	    # Else Delete Item and commit
	    db.session.delete(del_item)
	    db.session.commit()
	    return "item Deleted", 200

	if request.method == 'GET':
	    items = [ i.serializeitem for i in
	              db.session.query(Bucketitems).
	              filter(
	                 	 Bucketlist.creator == uid,
	                 	 Bucketlist.id == id,
	                 	 Bucketitems.id == item_id
	             		)
	            ]
	    if len(items) == 0:
	        return jsonify({'Error': 'No Item Found'}), 404
	    return jsonify(items = items), 200


@app.route("/")
def index():
    '''index page route index.html'''
    return jsonify({"info": "welcome Please Login "}), 200

@app.route('/api/users', methods = ['POST'])
def new_user():
    '''Route to Sign up page'''
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) 
    if Users.query.filter_by(username = username).first() is not None:
        abort(400)  
    user = Users(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201

# Route to Login Page
@app.route("/auth/login", methods = ["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # try to authenticate with username/password
    user = Users.query.filter_by(username = username).first()
    if user:
        confirm = user.verify_password(password)
        if confirm:
        	# Change logged flag to True
            user.logged = True
            db.session.commit()
            g.user = user
            token = g.user.generate_auth_token()
            return jsonify({'token': token.decode('ascii')}), 200
        return "wrong Password" 
    return "User was not found"

@app.route("/auth/logout", methods = ['GET'])
@auth.login_required
def logout():
    username = g.user.username
    user = Users.query.filter_by(username = username).first()
    user.logged = False
    db.session.commit()
    user = Users.query.filter_by(username = username).first()
    return "logged out %s" % user.username


if __name__ == "__main__":
    app.run(debug=True)
