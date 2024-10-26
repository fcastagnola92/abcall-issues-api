from typing import List, Optional
from flaskr.domain.interfaces import IssueRepository
from flaskr.domain.models import Issue

class IssueMockRepository(IssueRepository):
    def __init__(self, issuesMock: list[Issue]):
        super().__init__()
        self.issues = issuesMock


    def list_issues_period (self,user_id,year, month) -> List[Issue]:
        return self.issues
    
    def list_issues_filtered(self, user_id, status, channel_plan_id,created_at, closed_at) -> List[Issue]:
        return self.issues
    
    def create_issue(self, issue_data, new_attachment):
        self.issues.append(issue_data)
        return issue_data