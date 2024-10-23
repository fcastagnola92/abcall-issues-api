from typing import List, Optional
from uuid import UUID
from ..models.issue import Issue

class IssueRepository:
    def list(self) -> List[Issue]:
        raise NotImplementedError
    
    def list_issues_period (self,user_id,year, month) -> List[Issue]:
        raise NotImplementedError
    
    def list_issues_filtered (self, user_id, status, channel_plan_id, created_at, closed_at) -> List[Issue]:
        raise NotImplementedError
    
    def create_issue(self, issue_data: dict) -> Issue:
        raise NotImplementedError
