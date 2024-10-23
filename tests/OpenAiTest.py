import unittest
from unittest.mock import patch, MagicMock
from flaskr.application.openAiService import OpenAIService

class TestOpenAIService(unittest.TestCase):

    @patch('requests.post')
    def test_ask_chatgpt_success(self, mock_post):
        """
        Test ask_chatgpt method when the API responds with a successful answer.
        """
        # Mock response from OpenAI API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'This is the answer from ChatGPT'}}]
        }
        mock_post.return_value = mock_response

        # Instantiate the service
        openai_service = OpenAIService()

        # Call the method
        result = openai_service.ask_chatgpt("What is AI?")

        # Assertions
        self.assertEqual(result, "This is the answer from ChatGPT")
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_ask_chatgpt_failure(self, mock_post):
        """
        Test ask_chatgpt method when the API responds with an error.
        """
        # Mock response with a failure status code
        mock_response = MagicMock()
        mock_response.status_code = 500  # Simulating server error
        mock_post.return_value = mock_response

        # Instantiate the service
        openai_service = OpenAIService()

        # Call the method
        result = openai_service.ask_chatgpt("What is AI?")

        # Assertions
        self.assertIsNone(result)  # Expect None when the API fails
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_ask_chatgpt_exception(self, mock_post):
        """
        Test ask_chatgpt method when an exception occurs during the request.
        """
        # Simulate an exception when calling the OpenAI API
        mock_post.side_effect = Exception("Network error")

        # Instantiate the service
        openai_service = OpenAIService()

        # Call the method
        result = openai_service.ask_chatgpt("What is AI?")

        # Assertions
        self.assertIsNone(result)  # Expect None when an exception occurs
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_ask_chatgpt_invalid_json(self, mock_post):
        """
        Test ask_chatgpt method when the API returns an invalid JSON response.
        """
        # Mock response with invalid JSON
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")  # Simulate JSON parsing error
        mock_post.return_value = mock_response

        # Instantiate the service
        openai_service = OpenAIService()

        # Call the method
        result = openai_service.ask_chatgpt("What is AI?")

        # Assertions
        self.assertIsNone(result)  # Expect None when JSON parsing fails
        mock_post.assert_called_once()

