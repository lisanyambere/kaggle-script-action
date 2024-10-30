import unittest
from unittest.mock import patch
import requests
from fetch_data import fetch_data

class TestFetchData(unittest.TestCase):

	@patch('requests.get')
	def test_fetch_data_success(self, mock_get):
		mock_response = unittest.mock.Mock()
		mock_response.raise_for_status.return_value = None  # Simulate no HTTP error
		mock_response.json.return_value = {"userId": 1, "id": 1, "title": "Test Post", "body": "This is a test."}
		mock_get.return_value = mock_response

		url = "https://jsonplaceholder.typicode.com/posts/1"
		result = fetch_data(url)

		self.assertEqual(result, {"userId": 1, "id": 1, "title": "Test Post", "body": "This is a test."})

	@patch('requests.get')
	def test_fetch_data_http_error(self, mock_get):
		mock_response = unittest.mock.Mock()
		mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
		mock_get.return_value = mock_response

		url = "https://jsonplaceholder.typicode.com/posts/1"
		result = fetch_data(url)

		self.assertIsNone(result)

	@patch('requests.get')
	def test_fetch_data_request_exception(self, mock_get):
		mock_get.side_effect = requests.exceptions.RequestException("Network error")

		url = "https://jsonplaceholder.typicode.com/posts/1"
		result = fetch_data(url)

		self.assertIsNone(result)


if __name__ == '__main__':
	unittest.main()
