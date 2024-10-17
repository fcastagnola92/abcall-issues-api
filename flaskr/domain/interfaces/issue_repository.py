from typing import List, Optional
from uuid import UUID
from ..models.issue import Issue

class IssueRepository:
    def list(self) -> List[Issue]:
        raise NotImplementedError
    
    def list_issues_period (self,user_id,year, month) -> List[Issue]:
        raise NotImplementedError