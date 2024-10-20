from sqlalchemy import create_engine,extract, func
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from ...utils import Logger
from ...domain.models import Issue
from ...domain.interfaces import IssueRepository
from ...infrastructure.databases.model_sqlalchemy import Base, IssueModelSqlAlchemy
log = Logger()
from ...domain.constants import ISSUE_STATUS_SOLVED

class IssuePostgresqlRepository(IssueRepository):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def list_issues_period (self,user_id,year, month) -> List[Issue]:
        session = self.Session()
        try:
            issues=session.query(IssueModelSqlAlchemy).filter(
                extract('year', IssueModelSqlAlchemy.created_at) == year,
                extract('month', IssueModelSqlAlchemy.created_at) == month,
                IssueModelSqlAlchemy.status == ISSUE_STATUS_SOLVED,
                IssueModelSqlAlchemy.auth_user_id==user_id).all()
            
            return [self._from_model(issue_model) for issue_model in issues]
        finally:
            session.close()

    def create_issue(self, issue:Issue):
        try:
            session = self.Session()
            session.add(self._to_model(issue))
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()



    def _from_model(self, model: IssueModelSqlAlchemy) -> Issue:
        return Issue(
            id=model.id,
            auth_user_id=model.auth_user_id,
            auth_user_agent_id=model.auth_user_agent_id,
            status=model.status,
            subject=model.subject,
            description=model.description,
            created_at=model.created_at,
            closed_at=model.closed_at,
            channel_plan_id=model.channel_plan_id
        )
    


    
    def _to_model(self,issue:Issue)->IssueModelSqlAlchemy:
        return IssueModelSqlAlchemy(
            id=issue.id,
            auth_user_id=issue.auth_user_id,
            auth_user_agent_id=issue.auth_user_agent_id,
            status=issue.status,
            subject=issue.subject,
            description=issue.description,
            created_at=issue.created_at,
            closed_at=issue.closed_at,
            channel_plan_id=issue.channel_plan_id
        )


    