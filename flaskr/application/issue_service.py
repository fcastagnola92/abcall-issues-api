from typing import List
import requests
from uuid import UUID
import uuid
from datetime import datetime
from typing import TypedDict
from ..domain.interfaces.issue_repository import IssueRepository
from ..domain.models import Issue
from ..utils import Logger
from  config import Config
from .auth_service import AuthService
from ..utils import Logger
log = Logger()
class Status(TypedDict):
    id: UUID
    name: str
   
class IssueStatus:
    NEW = {"id": UUID("00000000-0000-0000-0000-000000000001"), "name": "New"}
    IN_PROGRESS = {"id": UUID("00000000-0000-0000-0000-000000000002"), "name": "In Progress"}
    RESOLVED = {"id": UUID("00000000-0000-0000-0000-000000000003"), "name": "Resolved"}
    CLOSED = {"id": UUID("00000000-0000-0000-0000-000000000004"), "name": "Closed"}

    ALL_STATUSES = [NEW, IN_PROGRESS, RESOLVED, CLOSED]
class IssueService:
    def __init__(self, issue_repository: IssueRepository=None):
        self.log = Logger()
        self.issue_repository=issue_repository

    def list_issues_period(self, customer_id, year, month):
        auth_service=AuthService()
        list_user_customer=auth_service.get_users_by_customer_list(customer_id)
        self.log.info(f'list user customer {list_user_customer}')
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

    def create_issue(self, auth_user_id: uuid, auth_user_agent_id: uuid, subject: str, description: str) -> uuid:
        if not auth_user_id or not subject or not description or not auth_user_agent_id:
            raise ValueError("All fields are required to create an issue.")
            
        new_issue = Issue(
            id=uuid.uuid4(),
            auth_user_id=auth_user_id,
            auth_user_agent_id=auth_user_agent_id,
            status=IssueStatus.NEW["id"],
            subject=subject,
            description=description,
            created_at=datetime.utcnow(),
            closed_at=None,
            channel_plan_id=None
        )

        issue_id = self.issue_repository.create_issue(new_issue)
        return issue_id