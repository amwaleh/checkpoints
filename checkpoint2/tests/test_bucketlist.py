from flask import Flask, g
import flask.ext.testing
from flask.ext.sqlalchemy import SQLAlchemy
import sys
sys.path.append('.')
from faker import Factory
from api.config import TEST_DB
from api.bucketlist import app
from api.models import db, Users, Bucketlist, Bucketitems
import unittest
import json


fake = Factory.create()
class BucketlistTestCase(unittest.TestCase):
    username = fake.name()
    password = fake.password()
    # Create the app
    def create_app(self):
        return create_app(self)

    # set up the app config database and
    @classmethod
    def setUpClass(self):
        with app.test_request_context():
            app.config['SECRET_KEY'] = "development-test-Key"
            app.config['TESTING'] = True
            # change config to use test database
            app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
            self.app = app.test_client()
            token = ''
            header = ''
            db.init_app(app)
            db.session.close()
            db.create_all()

     # Clean up
    @classmethod
    def tearDownClass(self):
        with app.test_request_context():
            db.session.close()
            db.drop_all()
            db.session.remove()

    def test_0_home_page(self):
        res = self.app.get('/')
        assert 'info' in res.data
        assert res.status_code == 200

    def test_0_1_Unauthorized_user(self):
        # check bucketlist
        res = self.app.get('/bucketlists')
        assert res.status_code == 401
        # check endpoint for token
        res = self.app.get('/api/token')
        assert res.status_code == 401

    def test_2_0_create_user(self):
        data = json.dumps(
            {"username": self.username, "password": self.password})
        res = self.app.post(
            '/api/users', data = data, content_type='application/json')
        # Check if the user has been added
        with app.test_request_context():
            user = Users.query.first()
        assert user.username == self.username
        assert res.status_code == 201

    def test_2_1_login(self):
        data = json.dumps(
            {"username": self.username, "password": self.password})
        res = self.app.post(
            '/auth/login', data = data, content_type='application/json')
        assert res.status_code == 200
        assert 'token' in res.data
        ''' if token is returned then user has been looged in
            decode json object
        '''
        json_data = json.loads(res.data)
        self.__class__.token = json_data['token']
        # try acessing a page once logged in
        data = json.dumps(
            {"username": self.username, "password": self.password})
        # Try accessing an authenicated page
        res = self.app.get('/bucketlists')
        assert res.status_code == 401

    def test_2_2_token_authenication(self):
        '''Access Page with Token'''
        self.__class__.header = {
            'Content-Type': 'application/json',
            'token': self.__class__.token
        }
        res = self.app.get('/bucketlists', headers = self.__class__.header)
        assert res.status_code == 200
        assert 'Bucketlist' in res.data

    def test_3_0_bucketlist_addition(self):
        ''' Test addition of bucketlist '''
        data = json.dumps({'name': "Test_list"})
        res = self.app.post(
            '/bucketlists', data = data, headers = self.__class__.header)
        with app.test_request_context():
            bucket = Bucketlist.query.first()
        redirect = self.app.get(res.location, headers = self.__class__.header)
        endpoint = self.app.get(
            "/bucketlists/{}".format(bucket.id), headers = self.__class__.header)
        assert res.status_code == 302
        assert redirect.data == endpoint.data
        assert bucket.name == json.loads(data)['name']

    def test_3_1_bucketlist_update(self):
        ''' Updates bucketlist and checks if out get request reflects the change'''
        name = "Test_update"
        data = json.dumps({'name': name})
        with app.test_request_context():
            bucket = Bucketlist.query.first()
        index = bucket.id
        res = self.app.put(
            '/bucketlists/{}'.format(index), data = data, headers = self.__class__.header)
        req = self.app.get(
            "/bucketlists/{}".format(index), headers = self.__class__.header)
        data = json.loads(req.data)['Bucketlist']
        assert res.status_code == 201
        assert name in data[0]

    def test_3_2_item_addition(self):
        item = "Item1"
        data = json.dumps({'name': item})
        with app.test_request_context():
            bucket = Bucketlist.query.first()
            index = bucket.id
            res = self.app.post("/bucketlists/{}/items".format(index),
                                data = data, headers = self.__class__.header)
            assert res.status_code == 201
            items = Bucketitems.query.first()
            res = self.app.get("/bucketlists/{}/items/{}".format(index, items.id),
                               data = data, headers = self.__class__.header)
            json_data = json.loads(res.data)['items'][0]
            assert item == json_data['name']

    def test_3_3_item_update(self):
        item = "Item-Updated"
        data = json.dumps({'name': item})
        with app.test_request_context():
            bucket = Bucketlist.query.first()
            items = Bucketitems.query.first()
            res = self.app.put(
                "/bucketlists/{}/items/{}".format(bucket.id, items.id),
                data = data, headers = self.__class__.header
            )
            assert res.status_code == 201
            res = self.app.get(
                "/bucketlists/{}/items/{}".format(bucket.id, items.id),
                data = data, headers = self.__class__.header
            )
            json_data = json.loads(res.data)['items'][0]
            assert item == json_data['name']

    def test_3_4_item_deletion(self):
        with app.test_request_context():
            bucket = Bucketlist.query.first()
            items = Bucketitems.query.first()
            res = self.app.delete(
                                    "/bucketlists/{}/items/{}".format(bucket.id, items.id),
                                    headers = self.__class__.header
                                 )
            res = self.app.get(
                                "/bucketlists/{}/items/{}".format(bucket.id, items.id),
                                headers = self.__class__.header
                              )
            items = Bucketitems.query.first()
            assert items is None

    def test_4_0_pages(self):
        for num in range(1, 10):
            listname = fake.name()
            data = json.dumps({'name': listname})
            req = self.app.post(
                '/bucketlists', data = data, headers = self.__class__.header)
            with app.test_request_context():
                bucket = Bucketlist.query.first()
            for lnum in range(1, 5):
                items = fake.word()
                data = json.dumps({'name': items})
                res = self.app.post(
                    "/bucketlists/{}/items".format(bucket.id),
                    data = data, headers = self.__class__.header
                )
        page = 1
        req = self.app.get(
                            "/bucketlists?page={}".format(page),
                            headers = self.__class__.header
                          )
        data = json.loads(req.data)
        data = data['Bucketlist'][0]
        assert 'current_page' in data
        assert data['current_page'] == page

    def test_5_0_bucketlist_delete(self):
        '''Deletes a bucketlist by index'''
        with app.test_request_context():
            bucket = Bucketlist.query.first()
            index = bucket.id
            req = self.app.delete(
                "/bucketlists/{}".format(index),
                headers = self.__class__.header
            )
            bucket = Bucketlist.query.get(index)
            assert bucket == None
            assert req.status_code == 401

    def test_6_logout(self):
        req = self.app.get("/auth/logout", headers = self.__class__.header)
        req = self.app.get("/bucketlists", headers = self.__class__.header)
        with app.test_request_context():
            user = Users.query.filter_by(username=self.username).first()
        assert user.logged == False
        assert req.status_code == 401

if __name__ == '__main__':
    unittest.main()
