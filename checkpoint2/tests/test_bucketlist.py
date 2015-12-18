from flask import Flask, g
from flask.ext.testing import TestCase
from flask.ext.sqlalchemy import SQLAlchemy
import sys

sys.path.append('.')
from faker import Factory
from api.config import TEST_DB
from api.bucketlist import app
from api.models import db, users
import unittest
import json
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

fake = Factory.create()
class BucketlistTestCase(unittest.TestCase):


    username = fake.name()
    password = fake.password()
   
    

    # Create the app
    def create_app(self):
        return create_app(self)
    # set up the app config database and 
    @classmethod
    def  setUpClass(self):
        with app.test_request_context():
            app.config['SECRET_KEY'] = "development-test-Key"
            app.config['TESTING'] = True
            # change config to use test database
            app.config['SQLALCHEMY_DATABASE_URI']= TEST_DB
            self.app = app.test_client()
            self.token = ''
            db.init_app(app) 
            #db.session.close() 
            db.create_all()
     # Clean up        
    @classmethod
    def tearDownClass(self):
        with app.test_request_context():
            db.session.close()
            db.drop_all()
            db.session.remove()
       
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

    def test_login(self) :
        data=json.dumps({"username": self.username, "password": self.password})
        res = self.app.post('/auth/login', data=data, content_type='application/json')
        assert res.status_code == 200
        assert 'token' in res.data
        # if token is returned then user has been looged in 
        # decode json object
        json_data = json.loads(res.data)
        app.token = json_data['token']
        # try acessing a page once logged in 
        data=json.dumps({"username": self.username, "password": self.password})
        # Try accessing an authenicated page 
        res = self.app.get('/bucketlists')
        assert res.status_code == 401

    def test_token_authenication (self):
        # Access Page with Token
        header ={
                    'Content-Type':'application/json' ,
                    'token': app.token
                }
        # Try accessing page with Token
        res = self.app.get('/bucketlists',headers=header)
        assert res.status_code == 200
        assert 'Bucketlist' in res.data
        

    def test_bucketlist_addition(self):
        data ={
                'name' : "Test_list"

              }
        pass
    def test_bucketlist_update(self):
        pass
    def test_bucketlist_delete(self):
        pass

    def test_item_addition(self):
        pass
    def test_item_update(self):
        pass
    def test_item_deletion(self):
        pass

    def test_pages(self):
        pass

    def test_page_range(self):
        pass

    def test_page_limit(self):
        pass
    def test_bucketlist_search(self):
        pass
    










    


    



    

    

if __name__ == '__main__':
    unittest.main()
