import unittest
from unittest.mock import patch
from http import HTTPStatus
from io import BytesIO
from faker import Faker
from flaskr.app import app
from builder import FindIssueBuilder, IssueBuilder

fake = Faker()
class IssueIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True
        


    
    def test_should_return_not_found_when_the_get_path_does_not_exist(self):
        data = {
            'auth_user_id': fake.uuid4(),
            'auth_user_agent_id': fake.uuid4(),
            'subject': fake.word(),
            'description': fake.sentence()
        }
        error_message = "Action not found"

        response = self.client.get('/issue/getFakePath', content_type='multipart/form-data', data=data)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json["message"], error_message)



        