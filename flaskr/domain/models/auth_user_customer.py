from uuid import UUID
from typing import Optional
from datetime import datetime
class AuthUserCustomer:
    """
    This class represent a relationship betweeen user and company
    Attributes:
        id (UUID) : issue id
        auth_user_id (UUID): user  id
        customer_id (UUID): customer id
    """
    def __init__(self, id:UUID,auth_user_id:UUID,customer_id:UUID):
        self.id=id
        self.auth_user_id=auth_user_id
        self.customer_id=customer_id


    def to_dict(self):
        return {
            'id': str(self.id),
            'auth_user_id': str(self.auth_user_id),
            'customer_id': str(self.customer_id)
        }