import unittest
from unittest.mock import patch
import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    @patch('server.signature_compass.requests.get')
    def test_get_text_signature(self, mock_get):
        # Mock response for requests.get
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            'results': [{'text_signature': 'mocked response'}]
        }

        # Define a test hex value
        test_hex = "1a2b3c4d"

        # Send a GET request to the route with the test hex
        response = self.app.get(f'/get-text-signature?hex={test_hex}')

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the response data matches the mocked response
        expected_response = 'mocked response'
        self.assertEqual(response.data.decode(), expected_response)

        # Verify that requests.get was called with the correct URL
        mock_get.assert_called_once_with(f'http://www.4byte.directory/api/v1/signatures/?hex_signature={test_hex}')

    @patch('server.signature_compass.list_signature')
    def test_list_signature_default(self, mock_list_signature):
        # Mock the return value of the list_signature method
        mock_list_signature.return_value = 'mocked response'

        # Simulate a request
        response = self.app.get('/list-signature?text=test_signature')

        # Assert that the mock method was called with the right parameters
        mock_list_signature.assert_called_once_with('test_signature', True, False)

        # Assert based on your expected response
        self.assertEqual(response.data, b'mocked response')

    @patch('server.signature_compass.list_signature')
    def test_list_signature_exact_match_false(self, mock_list_signature):
        # Mock the return value of the list_signature method
        mock_list_signature.return_value = 'mocked response'

        # Simulate a request
        response = self.app.get('/list-signature?text=test_signature&exact=False')

        # Assert that the mock method was called with the right parameters
        mock_list_signature.assert_called_once_with('test_signature', False, False)

        # Assert based on your expected response
        self.assertEqual(response.data, b'mocked response')

    @patch('server.signature_compass.list_signature')
    def test_list_signature_exact_match_true(self, mock_list_signature):
        # Mock the return value of the list_signature method
        mock_list_signature.return_value = 'mocked response'

        # Simulate a request
        response = self.app.get('/list-signature?text=test_signature&exact=TRUE')

        # Assert that the mock method was called with the right parameters
        mock_list_signature.assert_called_once_with('test_signature', True, False)

        # Assert based on your expected response
        self.assertEqual(response.data, b'mocked response')

    @patch('server.signature_compass.list_signature')
    def test_list_signature_case_sensitive_false(self, mock_list_signature):
        # Mock the return value of the list_signature method
        mock_list_signature.return_value = 'mocked response'

        # Simulate a request
        response = self.app.get('/list-signature?text=test_signature&exact=TRUE&case_sensitive=False')

        # Assert that the mock method was called with the right parameters
        mock_list_signature.assert_called_once_with('test_signature', True, False)

        # Assert based on your expected response
        self.assertEqual(response.data, b'mocked response')

    @patch('server.signature_compass.list_signature')
    def test_list_signature_case_sensitive_true(self, mock_list_signature):
        # Mock the return value of the list_signature method
        mock_list_signature.return_value = 'mocked response'

        # Simulate a request
        response = self.app.get('/list-signature?text=test_signature&exact=TRUE&case_sensitive=True')

        # Assert that the mock method was called with the right parameters
        mock_list_signature.assert_called_once_with('test_signature', True, True)

        # Assert based on your expected response
        self.assertEqual(response.data, b'mocked response')

    @patch('server.signature_compass.submit_signature')
    def test_submit_signature(self, mock_submit_signature):
        # Mock the return value of the list_signature method
        mock_submit_signature.return_value = 'mocked response'

        # Simulate a request
        response = self.app.post('/submit-signature?signature=test_signature')

        # Assert that the mock method was called with the right parameters
        mock_submit_signature.assert_called_once_with('test_signature')

        # Assert based on your expected response
        self.assertEqual(response.data, b'mocked response')


if __name__ == '__main__':
    unittest.main()
