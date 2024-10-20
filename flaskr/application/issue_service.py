from typing import List
from ..domain.models import Issue
import requests
from ..domain.interfaces.issue_repository import IssueRepository
import uuid
from datetime import datetime
from ..utils import Logger
from  config import Config
from .auth_service import AuthService

class IssueService:
    def __init__(self, issue_repository: IssueRepository=None):
        self.log = Logger()
        self.issue_repository=issue_repository

    def list_issues_period(self, customer_id, year, month):
        auth_service=AuthService()
        list_user_customer=auth_service.get_users_by_customer_list(customer_id)
        issues=[]
        if list_user_customer:
            for item in list_user_customer:
                issues.extend(self.issue_repository.list_issues_period(item.auth_user_id,year,month))
            return issues
        else:
            return None
        
    def list_issues_filtered(self, customer_id, status=None, channel_plan_id=None, created_at=None, closed_at=None):
        auth_service = AuthService()
        list_user_customer = auth_service.get_users_by_customer_list(customer_id)
        issues = []
        
        if list_user_customer:
            for item in list_user_customer:
                user_issues = self.issue_repository.list_issues_filtered(
                    user_id=item.auth_user_id, 
                    status=status, 
                    channel_plan_id=channel_plan_id, 
                    created_at=created_at, 
                    closed_at=closed_at
                )
                issues.extend(user_issues)
            return issues
        else:
            return None

    