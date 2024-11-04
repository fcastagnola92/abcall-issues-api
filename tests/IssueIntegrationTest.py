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
        





        