import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from flaskr.infrastructure.databases.issue_postresql_repository import IssuePostgresqlRepository
from flaskr.domain.models import Issue, IssueAttachment

class TestIssuePostgresqlRepository(unittest.TestCase):
    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.sessionmaker')
    def setUp(self, mock_sessionmaker, mock_create_engine):
        mock_create_engine.return_value = MagicMock()
        self.repo = IssuePostgresqlRepository('mock_connection_string')
        self.repo.Session = MagicMock()

    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.sessionmaker')
    def test_list_issues_period(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value

        mock_issue = Issue(
            id=uuid4(),
            auth_user_id=uuid4(),
            auth_user_agent_id=uuid4(),
            status='SOLVED',
            subject='Test Subject',
            description='Test Description',
            created_at='2023-01-01',
            closed_at='2023-01-02',
            channel_plan_id=uuid4()
        )
        mock_session_instance.query.return_value.filter.return_value.all.return_value = [mock_issue]

        result = self.repo.list_issues_period(user_id=mock_issue.auth_user_id, year=2023, month=1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].subject, 'Test Subject')
        mock_session_instance.query.assert_called_once()

    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.sessionmaker')
    def test_list_issues_filtered(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value

        mock_issue = Issue(
            id=uuid4(),
            auth_user_id=uuid4(),
            auth_user_agent_id=uuid4(),
            status='OPEN',
            subject='Filtered Issue',
            description='Filtered Description',
            created_at='2023-03-01',
            closed_at='2023-03-05',
            channel_plan_id=uuid4()
        )
        mock_session_instance.query.return_value.filter.return_value.all.return_value = [mock_issue]

        result = self.repo.list_issues_filtered(user_id=mock_issue.auth_user_id, status='OPEN')

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['subject'], 'Filtered Issue')
        mock_session_instance.query.assert_called_once()

    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.sessionmaker')
    def test_create_issue(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value

        mock_issue = Issue(
            id=uuid4(),
            auth_user_id=uuid4(),
            auth_user_agent_id=uuid4(),
            status='NEW',
            subject='New Issue',
            description='New Description',
            created_at='2023-04-01',
            closed_at=None,
            channel_plan_id=uuid4()
        )
        
        self.repo.create_issue(mock_issue)
        
        mock_session_instance.add.assert_called_once()
        mock_session_instance.commit.assert_called()

    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.sessionmaker')
    def test_find(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value
        
        mock_issue = Issue(
            id=uuid4(),
            auth_user_id=uuid4(),
            auth_user_agent_id=uuid4(),
            status='CLOSED',
            subject='Found Issue',
            description='Found Description',
            created_at='2023-05-01',
            closed_at='2023-05-10',
            channel_plan_id=uuid4()
        )
        mock_session_instance.query.return_value.join.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [mock_issue]
        mock_session_instance.query.return_value.filter.return_value.count.return_value = 1

        result = self.repo.find(user_id=mock_issue.auth_user_id, page=1, limit=10)
        
        self.assertEqual(result['total_pages'], 1)
        self.assertTrue(result['has_next'])
        self.assertEqual(result['data'][0]['subject'], 'Found Issue')
        mock_session_instance.query.assert_called()

    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postgresql_repository.sessionmaker')
    def test_list_top_issues_by_user(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value
        
        mock_issue_description = 'Top Issue Description'
        mock_session_instance.query.return_value.filter.return_value.order_by.return_value.limit.return_value.subquery.return_value.c.description.return_value.distinct.return_value.all.return_value = [(mock_issue_description,)]

        result = self.repo.list_top_issues_by_user(user_id=uuid4())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (mock_issue_description,))
        mock_session_instance.query.assert_called()