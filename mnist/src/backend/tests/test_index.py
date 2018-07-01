import unittest

# your test cases
import urllib
from flask_testing import TestCase

# add parent module path
import os, sys, io, requests
sys.path.append('..')
from utils import *
from http import HTTPStatus

from sdm import app

class HelloTest(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        self.id = "admin"
        self.pw = "admin"
        self.level = "A"
        res = requests.post("http://flask-skp:5000/v1/tokens", data = {
            'id' : self.id,
            'pw' : self.pw,
            'level' : self.level
        })
        self.assertEqual(res.status_code, HTTPStatus.CREATED)
        res_json = res.json()
        self.access_token = res_json['access_token']
        self.refresh_token = res_json['refresh_token']
        return

    def tearDown(self):
        return

    def test_001(self):
        f = open('/root/mnt/dfs/notebooks-skp/mnist/src/backend/tests/5.jpg', 'rb')
        io_img = io.BytesIO(f.read())      
        
        res = self.client.post("/v1/dnn", 
            headers = { 'Authorization' : "Bearer {}".format(self.access_token) },
            content_type = 'multipart/form-data',
            data = {
                'file': (io_img, '5.jpg')
            })
        print_response(self, res)
        self.assertEqual(res.status_code, HTTPStatus.OK)

    def test_002(self):
        f = open('/root/mnt/dfs/notebooks-skp/mnist/src/backend/tests/5.jpg', 'rb')
        io_img = io.BytesIO(f.read())      
        
        res = self.client.post("/v1/cnn", 
            headers = { 'Authorization' : "Bearer {}".format(self.access_token) },
            content_type = 'multipart/form-data',
            data = {
                'file': (io_img, '5.jpg')
            })
        print_response(self, res)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        
if __name__ == '__main__':
    unittest.main()
