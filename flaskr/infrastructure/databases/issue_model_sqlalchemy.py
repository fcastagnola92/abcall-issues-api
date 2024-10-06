from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class IssueModelSqlAlchemy(Base):
    __tablename__ = 'issues'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)