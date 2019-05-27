import json
import unittest
import app as my_app
from flask import *

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = my_app.app.test_client()

    def test_book_list(self):
        my_app.books = []
        resp = self.app.get('api/books/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(content), 0)
        self.assertEqual(content, [])

    def test_that_title_and_author_required_fields(self):
        # Test
        resp = self.app.post('api/books/',
                             data=json.dumps({}),
                             content_type='application/json')
        self.assertEqual(b'{"error": "Field \'author\' and \'title\' are required."}', resp.get_data())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual('application/json', resp.content_type)

        resp = self.app.post('api/books/',
                             data=json.dumps({'author': 'Any Author'}),
                             content_type='application/json')
        self.assertEqual(b'{"error": "Field \'title\' is required."}', resp.get_data())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual('application/json', resp.content_type)

        resp = self.app.post('api/books/',
                             data=json.dumps({'title': 'Any Title'}),
                             content_type='application/json')
        self.assertEqual(b'{"error": "Field \'author\' is required."}', resp.get_data())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual('application/json', resp.content_type)

    def test_that_title_and_author_cannot_be_empty(self):
        post_data = {
            'author': '',
            'title': ''
        }
        resp = self.app.post('api/books/',
                             data=json.dumps(post_data),
                             content_type='application/json')
        self.assertEqual(b'{"error": "Field \'author\' and \'title\' cannot be empty."}', resp.get_data())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual('application/json', resp.content_type)

        post_data['author'] = 'Any Author'
        resp = self.app.post('api/books/',
                             data=json.dumps(post_data),
                             content_type='application/json')
        self.assertEqual(b'{"error": "Field \'title\' cannot be empty."}', resp.get_data())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual('application/json', resp.content_type)

        post_data['author'] = ''
        post_data['title'] = 'Any Title'
        resp = self.app.post('api/books/',
                             data=json.dumps(post_data),
                             content_type='application/json')
        self.assertEqual(b'{"error": "Field \'author\' cannot be empty."}', resp.get_data())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual('application/json', resp.content_type)

    def test_that_the_id_field_is_read_only(self):
        post_data = {
            'id': 1,
            'author': 'Any Author',
            'title': 'Any Title'
        }
        resp = self.app.post('api/books/',
                             data=json.dumps(post_data),
                             content_type='application/json')
        self.assertEqual(b'{"error": "You cannot set \'id\' field."}', resp.get_data())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual('application/json', resp.content_type)

    def test_that_you_can_create_a_book_via_PUT(self):
        pass

    def test_you_cannot_create_a_duplicate_book(self):
        post_data = {
            'author': 'Any Author',
            'title': 'Any Title'
        }
        resp = self.app.post('api/books/',
                             data=json.dumps(post_data),
                             content_type='application/json')
        #self.assertEqual(b'{"id": 34, "author": "Any Author", "title": "Any Title"}', resp.get_data())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual('application/json', resp.content_type)

        resp = self.app.post('api/books/',
                             data=json.dumps(post_data),
                             content_type='application/json')
        self.assertEqual(b'{"error": "Another book with similar title and author already exists."}', resp.get_data())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual('application/json', resp.content_type)

