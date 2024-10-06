from typing import List, Optional
from uuid import UUID
from ..models.issue import Issue

class IssueRepository:
    def list(self) -> List[Issue]:
        raise NotImplementedError