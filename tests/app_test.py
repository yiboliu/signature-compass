import unittest
from unittest.mock import patch
import app
import json
import signature_compass


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    @patch('signature_compass.requests.get')
    def test_get_text_signature(self, mock_get):
        # Mock response for requests.get
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            'results': [{'text_signature': 'mocked response'}]
        }

        # Define a test hex value
        test_hex = "1a2b3c"

        # Send a GET request to the route with the test hex
        response = self.app.get(f'/get-text-signature?hex={test_hex}')

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the response data matches the mocked response
        expected_response = 'mocked response'
        self.assertEqual(response.data.decode(), expected_response)

        # Verify that requests.get was called with the correct URL
        mock_get.assert_called_once_with(f'http://www.4byte.directory/api/v1/signatures/?hex_signature={test_hex}')


if __name__ == '__main__':
    unittest.main()
