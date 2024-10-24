import unittest
from unittest.mock import patch, MagicMock
from uuid import UUID, uuid4
from datetime import datetime
from flaskr.application.issue_service import IssueService, IssueStatus
from flaskr.domain.models import Issue, IssueAttachment


class TestIssueService(unittest.TestCase):

    

   

    @patch('flaskr.application.openAiService.OpenAIService.ask_chatgpt')
    def test_ask_generative_ai(self, mock_ask_chatgpt):
        """
        Test ask_generative_ai method which uses OpenAIService.
        """

        mock_ask_chatgpt.return_value = "This is an AI response"


        issue_service = IssueService()


        result = issue_service.ask_generative_ai("What is AI?")


        self.assertEqual(result, "This is an AI response")

