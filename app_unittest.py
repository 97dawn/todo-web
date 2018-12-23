#-*- coding: utf-8 -*-
from app import app
import unittest
'''
Each unittest should be executed one by one
'''
class FlaskTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/',content_type='html/text')
        self.assertTrue(b'main' in response.data)

    def test_add1(self):
        tester = app.test_client(self)
        response = tester.get('/add?title=title1&content=content1', content_type='html/text')
        self.assertTrue(b'title1' in response.data and b'content1' in response.data)

    def test_add2(self):
        tester = app.test_client(self)
        response = tester.get('/add?title=title2&content=content2', content_type='html/text')
        self.assertTrue(b'title2' in response.data and b'content2' in response.data)
    
    def test_add3(self):
        tester = app.test_client(self)
        response = tester.get('/add?title=title3&content=content3', content_type='html/text')
        self.assertTrue(b'title3' in response.data and b'content3' in response.data)

    def test_up1(self):
        tester = app.test_client(self)
        response = tester.get('/up/0', content_type='html/text')
        self.assertTrue(response.data.find(b'title1') < response.data.find(b'title2'))
    
    def test_up2(self):
        tester = app.test_client(self)
        response = tester.get('/up/1', content_type='html/text')
        self.assertTrue(response.data.find(b'title1') > response.data.find(b'title2'))
    
    def test_down1(self):
        tester = app.test_client(self)
        response = tester.get('/down/0', content_type='html/text')
        self.assertTrue(response.data.find(b'title1') < response.data.find(b'title2'))
    
    def test_down3(self):
        tester = app.test_client(self)
        response = tester.get('/down/2', content_type='html/text')
        self.assertTrue(response.data.find(b'title3') > response.data.find(b'title2'))

    def test_modify(self):
        tester = app.test_client(self)
        response = tester.get('/modify/0?title=title1&content=content11&due_date=Dec+10%2C+2018', content_type='html/text')
        self.assertTrue(b'2018-12-10' in response.data and b'content11' in response.data)
        # check alert
        self.assertTrue(b'alert' in response.data)

    def test_done(self):
        tester = app.test_client(self)
        response = tester.get('/done/0', content_type='html/text')
        self.assertTrue(response.data.find(b'title3') < response.data.find(b'title1'))
    
    def test_remove(self):
        tester = app.test_client(self)
        response = tester.get('/remove/2', content_type='html/text')
        self.assertTrue(b'title3' not in response.data)

if __name__=="__main__":
    unittest.main()