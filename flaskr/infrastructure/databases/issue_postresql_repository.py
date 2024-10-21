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

    def list_issues_filtered(self, user_id, status=None, channel_plan_id=None, created_at=None, closed_at=None):
        session = self.Session()
        try:            
            query = session.query(IssueModelSqlAlchemy).filter(IssueModelSqlAlchemy.auth_user_id == user_id)
        
            if status:
                query = query.filter(IssueModelSqlAlchemy.status == status)
            if channel_plan_id:
                query = query.filter(IssueModelSqlAlchemy.channel_plan_id == channel_plan_id)
            if created_at:
                query = query.filter(IssueModelSqlAlchemy.created_at >= created_at)
            if closed_at:
                query = query.filter(IssueModelSqlAlchemy.closed_at <= closed_at)

            issues_sqlalchemy = query.all()

            issues = [
                Issue(
                    id=issue_model.id,
                    auth_user_id=issue_model.auth_user_id,
                    auth_user_agent_id=issue_model.auth_user_agent_id,
                    status=issue_model.status,
                    subject=issue_model.subject,
                    description=issue_model.description,
                    created_at=issue_model.created_at,
                    closed_at=issue_model.closed_at,
                    channel_plan_id=issue_model.channel_plan_id
                ).to_dict() for issue_model in issues_sqlalchemy
            ]

            return issues

        finally:
            session.close()

    def create_issue(self, issue:Issue):
        try:
            session = self.Session()
            session.add(self._from_model(issue))
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def _from_model(self, model: Issue) -> IssueModelSqlAlchemy:
        return IssueModelSqlAlchemy(
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
