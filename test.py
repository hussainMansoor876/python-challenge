import unittest
import json

from challenge import app

class TestFamilyTreeAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_member(self):
        response = self.app.post('/add-member', json={'name': 'Jenny Doe'})
        print('json.loads(response.data)', json.loads(response.data))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['message'], 'Member Jenny Doe created')

    def test_create_existing_member(self):
        self.app.post('/add-member', json={'name': 'John Doe'})
        response = self.app.post('/add-member', json={'name': 'John Doe'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.data)['message'], 'Member John Doe already exist')

    def test_create_member_missing_name(self):
        response = self.app.post('/add-member', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'Name is required')

    def test_add_relationship(self):
        self.app.post('/add-member', json={'name': 'John Doe'})
        self.app.post('/add-member', json={'name': 'Jane Doe'})
        response = self.app.post('/add-relationship', json={'member1_name': 'John Doe', 'member2_name': 'Jane Doe', 'relation': 'SPOUSE'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['message'], 'Relationship defined between John Doe and Jane Doe')

    def test_add_relationship_missing_fields(self):
        response = self.app.post('/add-relationship', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'All fields are required')

    def test_get_relationship(self):
        self.app.post('/add-member', json={'name': 'John Doe'})
        self.app.post('/add-member', json={'name': 'Jane Doe'})
        self.app.post('/add-relationship', json={'member1_name': 'John Doe', 'member2_name': 'Jane Doe', 'relation': 'SPOUSE'})
        response = self.app.post('/get-relationship', json={'member1_name': 'John Doe', 'member2_name': 'Jane Doe'})
        print('response', json.loads(response.data))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['closest_count'], 1)

    def test_get_relationship_missing_fields(self):
        response = self.app.post('/get-relationship', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'Both member names are required')

if __name__ == '__main__':
    unittest.main()