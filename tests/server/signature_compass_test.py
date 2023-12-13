import unittest
from unittest.mock import patch
from server import signature_compass, utils


class TestSignatureCompass(unittest.TestCase):

    @patch('requests.get')
    def test_get_text_signature_valid_hex(self, mock_get):
        # Prepare a mock response
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'results': [{'text_signature': 'mocked text signature'}]
        }
        mock_get.return_value = mock_response

        # Call the function with a valid hex value
        hex_value = '0x12345678'
        result = signature_compass.get_text_signature(hex_value)

        # Assert that the request was made correctly and the result is as expected
        mock_get.assert_called_with(f'{signature_compass.url}?hex_signature={hex_value}')
        self.assertEqual(result, 'mocked text signature')

    def test_get_text_signature_short_hex(self):
        # Test with a hex string that is too short
        with self.assertRaises(ValueError):
            signature_compass.get_text_signature('123')

    @patch('requests.get')
    def test_get_text_signature_long_hex(self, mock_get):
        # Prepare a mock response for a long hex string
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {
            'results': [{'text_signature': 'mocked text signature for long hex'}]
        }
        mock_get.return_value = mock_response

        # Call the function with a long hex value
        long_hex_value = '0x123456789abcdef'
        result = signature_compass.get_text_signature(long_hex_value)

        # Assert that only the first 4 bytes are used and the result is as expected
        mock_get.assert_called_with(f'{signature_compass.url}?hex_signature=0x12345678')
        self.assertEqual(result, 'mocked text signature for long hex')

    @patch('requests.get')
    def test_list_signature_exact_match(self, mock_get):
        # Mock the response of requests.get
        mock_get.return_value.text = 'mocked response'

        # Test exact match
        result = signature_compass.list_signature('test_signature', exact=True, case_sensitive=False)

        # Assert the expected outcome
        self.assertEqual(result, 'mocked response')
        mock_get.assert_called_with(f'{signature_compass.url}?text_signature__iexact')

    @patch('requests.get')
    @patch('server.utils.analyze_regex')
    def test_list_signature_startswith(self, mock_analyze_regex, mock_get):
        # Set up the mock for analyze_regex
        mock_analyze_regex.return_value = utils.RegexType.START

        # Mock the response of requests.get
        mock_get.return_value.text = 'mocked response'

        # Test startswith pattern
        result = signature_compass.list_signature('^test', exact=False, case_sensitive=False)

        # Assert the expected outcome
        self.assertEqual(result, 'mocked response')
        mock_get.assert_called_with(f'{signature_compass.url}?text_signature__startswith')

    @patch('requests.get')
    @patch('server.utils.analyze_regex')
    def test_list_signature_istartswith(self, mock_analyze_regex, mock_get):
        # Set up the mock for analyze_regex
        mock_analyze_regex.return_value = utils.RegexType.START

        # Mock the response of requests.get
        mock_get.return_value.text = 'mocked response'

        # Test startswith pattern
        result = signature_compass.list_signature('^test', exact=False, case_sensitive=True)

        # Assert the expected outcome
        self.assertEqual(result, 'mocked response')
        mock_get.assert_called_with(f'{signature_compass.url}?text_signature__istartswith')

    @patch('requests.get')
    @patch('server.utils.analyze_regex')
    def test_list_signature_endswith(self, mock_analyze_regex, mock_get):
        # Set up the mock for analyze_regex
        mock_analyze_regex.return_value = utils.RegexType.END

        # Mock the response of requests.get
        mock_get.return_value.text = 'mocked response'

        # Test startswith pattern
        result = signature_compass.list_signature('^test', exact=False, case_sensitive=False)

        # Assert the expected outcome
        self.assertEqual(result, 'mocked response')
        mock_get.assert_called_with(f'{signature_compass.url}?text_signature__endswith')

    @patch('requests.get')
    @patch('server.utils.analyze_regex')
    def test_list_signature_iendswith(self, mock_analyze_regex, mock_get):
        # Set up the mock for analyze_regex
        mock_analyze_regex.return_value = utils.RegexType.END

        # Mock the response of requests.get
        mock_get.return_value.text = 'mocked response'

        # Test startswith pattern
        result = signature_compass.list_signature('^test', exact=False, case_sensitive=True)

        # Assert the expected outcome
        self.assertEqual(result, 'mocked response')
        mock_get.assert_called_with(f'{signature_compass.url}?text_signature__iendswith')

    @patch('server.utils.analyze_regex')
    def test_list_signature_unsupported(self, mock_analyze_regex):
        mock_analyze_regex.return_value = utils.RegexType.UNKNOWN
        with self.assertRaises(ValueError):
            signature_compass.list_signature(text_signature='123', exact=False)

    @patch('requests.post')
    @patch('server.signature_compass.list_signature')
    def test_submit_signature_success(self, mock_list_signature, mock_post):
        # Mock the post request response
        mock_post_response = unittest.mock.Mock()
        mock_post_response.ok = True
        mock_post.return_value = mock_post_response

        # Mock the list_signature function
        mock_list_signature.return_value = 'test_signature'

        # Test submission
        result = signature_compass.submit_signature('test_signature')

        # Assert that submission is successful
        self.assertTrue(result)

    @patch('requests.post')
    def test_submit_signature_failure(self, mock_post):
        # Mock the post request response
        mock_post_response = unittest.mock.Mock()
        mock_post_response.ok = False
        mock_post.return_value = mock_post_response

        # Test submission
        result = signature_compass.submit_signature('test_signature')

        # Assert that submission failed
        self.assertFalse(result)

    @patch('requests.post')
    @patch('server.signature_compass.list_signature')
    def test_submit_signature_not_found_in_db(self, mock_list_signature, mock_post):
        # Mock the post request response
        mock_post_response = unittest.mock.Mock()
        mock_post_response.ok = True
        mock_post.return_value = mock_post_response

        # Mock the list_signature function
        mock_list_signature.return_value = 'different_signature'

        # Test submission
        result = signature_compass.submit_signature('test_signature')

        # Assert that submission is reported as failure because it's not found in DB
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
