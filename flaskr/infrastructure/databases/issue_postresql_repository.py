from sqlalchemy import create_engine,extract, func
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from uuid import UUID
from ...domain.models import Issue
from ...domain.interfaces import IssueRepository
from ...infrastructure.databases.model_sqlalchemy import Base, IssueModelSqlAlchemy
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

    def list_issues_filtered(self, status=None, channel_plan_id=None, created_at=None, closed_at=None) -> List[Issue]:
        session = self.Session()
        try:
            query = session.query(IssueModelSqlAlchemy)
            
            # Agregar filtros opcionales
            if status:
                query = query.filter(IssueModelSqlAlchemy.status == status)
            if channel_plan_id:
                query = query.filter(IssueModelSqlAlchemy.channel_plan_id == channel_plan_id)
            if created_at:
                query = query.filter(IssueModelSqlAlchemy.created_at >= created_at)
            if closed_at:
                query = query.filter(IssueModelSqlAlchemy.closed_at <= closed_at)
            
            issues = query.all()
            
            return [self._from_model(issue_model) for issue_model in issues]
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
