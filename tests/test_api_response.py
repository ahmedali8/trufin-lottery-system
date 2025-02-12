import unittest
from unittest.mock import patch, Mock
import requests
from app.api.fetch_random_users import fetch_random_users
from app.utils.config import API_URL

class TestRandomUserAPI(unittest.TestCase):
    def setUp(self):
        """Set up sample data for testing"""
        self.sample_user = {
            "id": 1,
            "uid": "sample-uid",
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "test@email.com",
            "avatar": "https://example.com/avatar.png",
            "gender": "Other",
            "phone_number": "+1-555-555-5555",
            "date_of_birth": "2000-01-01",
            "employment": {
                "title": "Software Engineer",
                "key_skill": "Python"
            },
            "address": {
                "city": "Test City",
                "street_name": "Test Street",
                "street_address": "123 Test St",
                "zip_code": "12345",
                "state": "Test State",
                "country": "Test Country",
                "coordinates": {
                    "lat": 40.7128,
                    "lng": -74.0060
                }
            },
            "subscription": {
                "plan": "Premium",
                "status": "Active",
                "payment_method": "Credit card",
                "term": "Annual"
            }
        }

    @patch('requests.get')
    def test_response_structure(self, mock_get):
        """Test the basic structure and data types of the API response"""
        # Setup mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None

        # Test with different sizes
        for size in [1, 3, 5]:
            # Create response data with appropriate size
            mock_data = [self.sample_user for _ in range(size)]
            mock_response.json.return_value = mock_data
            mock_get.return_value = mock_response

            with self.subTest(size=size):
                # Get response
                result = fetch_random_users(size)

                # Validate basic structure
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), size)

                # Test each user object
                for user in result:
                    self._validate_user_structure(user)

    def _validate_user_structure(self, user):
        """Validate the structure and data types of a user object"""
        # Basic fields type validation
        self.assertIsInstance(user.get('id'), int)
        self.assertIsInstance(user.get('uid'), str)
        self.assertIsInstance(user.get('first_name'), str)
        self.assertIsInstance(user.get('last_name'), str)
        self.assertIsInstance(user.get('username'), str)
        self.assertIsInstance(user.get('email'), str)

        # Validate nested objects
        self.assertIn('employment', user)
        self.assertIsInstance(user['employment'], dict)
        self.assertIn('title', user['employment'])
        self.assertIn('key_skill', user['employment'])

        # Validate address
        self.assertIn('address', user)
        address = user['address']
        self.assertIsInstance(address, dict)
        self.assertIn('coordinates', address)
        self.assertIsInstance(address['coordinates'], dict)
        self.assertIsInstance(address['coordinates'].get('lat'), (int, float))
        self.assertIsInstance(address['coordinates'].get('lng'), (int, float))

        # Validate subscription
        self.assertIn('subscription', user)
        subscription = user['subscription']
        self.assertIsInstance(subscription, dict)
        self.assertIn('plan', subscription)
        self.assertIn('status', subscription)
        self.assertIn('payment_method', subscription)
        self.assertIn('term', subscription)

    def _validate_employment(self, employment):
        """Validate employment object structure"""
        self.assertIsInstance(employment, dict)
        self.assertIsInstance(employment.get('title'), str)
        self.assertIsInstance(employment.get('key_skill'), str)

    def _validate_address(self, address):
        """Validate address object structure"""
        self.assertIsInstance(address, dict)

        # Check basic address fields
        required_str_fields = ['city', 'street_name', 'street_address',
                             'zip_code', 'state', 'country']
        for field in required_str_fields:
            self.assertIsInstance(address.get(field), str)

        # Validate coordinates
        coords = address.get('coordinates', {})
        self.assertIsInstance(coords.get('lat'), (int, float))
        self.assertIsInstance(coords.get('lng'), (int, float))

    def _validate_subscription(self, subscription):
        """Validate subscription object structure"""
        self.assertIsInstance(subscription, dict)

        required_str_fields = ['plan', 'status', 'payment_method', 'term']
        for field in required_str_fields:
            self.assertIsInstance(subscription.get(field), str)

    @patch('requests.get')
    def test_error_handling(self, mock_get):
        """Test API error handling"""
        # Use actual requests exceptions
        error_cases = [
            requests.exceptions.ConnectionError("Connection failed"),
            requests.exceptions.HTTPError("404 Not Found"),
            requests.exceptions.Timeout("Request timed out"),
            # Proper JSON decode error
            requests.exceptions.JSONDecodeError("Invalid JSON", "", 0)
        ]

        for error in error_cases:
            with self.subTest(error=error):
                mock_get.side_effect = error
                result = fetch_random_users(3)
                # Should return empty list on error
                self.assertEqual(result, [])

    @patch('requests.get')
    def test_size_parameter(self, mock_get):
        """Test that the size parameter is correctly passed to the API"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        sizes_to_test = [1, 3, 5, 10]
        for size in sizes_to_test:
            fetch_random_users(size)
            mock_get.assert_called_with(f"{API_URL}?size={size}")

if __name__ == '__main__':
    unittest.main()
