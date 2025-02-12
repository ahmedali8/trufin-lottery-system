import unittest
from unittest.mock import patch, MagicMock
from app.db.db_connection import get_db_connection, close_connection
from app.utils.config import DB_CONFIG

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        """Reset the connection before each test"""
        # Access the global _connection variable through the module
        import app.db.db_connection as db_module
        db_module._connection = None

    def tearDown(self):
        """Clean up after each test"""
        close_connection()

    @patch('psycopg2.connect')
    def test_successful_connection(self, mock_connect):
        """Test successful database connection"""
        # Create a mock connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Get connection
        connection = get_db_connection()

        # Assertions
        mock_connect.assert_called_once_with(**DB_CONFIG)
        self.assertIsNotNone(connection)

        # Test connection reuse (should not create new connection)
        second_connection = get_db_connection()
        self.assertEqual(connection, second_connection)
        mock_connect.assert_called_once()  # Should still be called only once

    @patch('psycopg2.connect')
    def test_failed_connection(self, mock_connect):
        """Test database connection failure"""
        # Make the connection fail
        mock_connect.side_effect = Exception("Connection failed")

        # Attempt to get connection
        connection = get_db_connection()

        # Assertions
        mock_connect.assert_called_once_with(**DB_CONFIG)
        self.assertIsNone(connection)

    def test_close_connection(self):
        """Test closing the database connection"""
        # Create a mock connection first
        import app.db.db_connection as db_module
        mock_conn = MagicMock()
        db_module._connection = mock_conn

        # Close the connection
        close_connection()

        # Assertions
        mock_conn.close.assert_called_once()
        self.assertIsNone(db_module._connection)

    def test_close_nonexistent_connection(self):
        """Test closing when no connection exists"""
        # Ensure no connection exists
        import app.db.db_connection as db_module
        db_module._connection = None

        # This should not raise any errors
        close_connection()

if __name__ == '__main__':
    unittest.main()
