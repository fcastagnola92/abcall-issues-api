import unittest
from uuid import uuid4
from flaskr.domain.models.auth_user_customer import AuthUserCustomer

class TestAuthUserCustomer(unittest.TestCase):

    def setUp(self):
        
        self.id = uuid4()
        self.auth_user_id = uuid4()
        self.customer_id = uuid4()

        
        self.auth_user_customer = AuthUserCustomer(
            id=self.id,
            auth_user_id=self.auth_user_id,
            customer_id=self.customer_id
        )

    def test_initialization(self):
        
        self.assertEqual(self.auth_user_customer.id, self.id)
        self.assertEqual(self.auth_user_customer.auth_user_id, self.auth_user_id)
        self.assertEqual(self.auth_user_customer.customer_id, self.customer_id)

    def test_to_dict(self):
        
        expected_dict = {
            'id': str(self.id),
            'auth_user_id': str(self.auth_user_id),
            'customer_id': str(self.customer_id)
        }

        self.assertEqual(self.auth_user_customer.to_dict(), expected_dict)


