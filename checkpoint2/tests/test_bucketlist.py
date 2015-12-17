from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sys
from faker import Factory
sys.path.append('.')
from api import bucketlist 
from api.bucketlist import app
from api.models import db
import unittest
import json

fake = Factory.create()
class BucketlistTestCase(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = "postgres://"
    TESTING = True
    db = SQLAlchemy()

    username = fake.name()
    password = fake.password()
    
        
       
    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'
        app.config['SECRET_KEY'] = "development-Key"
        #app.config["JSON_SORT_KEYS"] = False
        
        
        return app

    def setUp(self):
       
        bucketlist.app.config['TESTING']= True
        self.app = bucketlist.app.test_client()
        self.client = bucketlist.app.test_client()

        with app.test_request_context():
                # Extensions like Flask-SQLAlchemy now know what the "current" app
            db.init_app(app)    # is while within this block. Therefore, you can now run........
            
        with app.test_request_context():
            db.create_all()
    
        
    def test_home_page(self):
        res =  self.app.get('/')
        assert 'info' in res.data
        assert res.status_code == 200

    def test_Unauthorized_user(self):
        # check bucketlist
        res = self.app.get('/bucketlists')
        assert res.status_code == 401
        # check endpoint for token
        res = self.app.get('/api/token')
        assert res.status_code == 401
        
    def test_create_user(self):
        
        data=json.dumps({"username": self.username, "password": self.password})
        res = self.app.post('/api/users', data=data, content_type='application/json' )
        assert res.status_code == 201
        # check if user has been added


    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all


    



    

    

if __name__ == '__main__':
    unittest.main()
