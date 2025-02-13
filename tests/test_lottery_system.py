import unittest
from unittest.mock import patch, MagicMock
from app.services.lottery_service import process_winners
from app.repositories.winner_repository import (
    create_versioned_table, insert_winner, get_winner_count, get_winners, get_new_version
)
from app.api.fetch_random_users import fetch_default_users
from app.utils.logger import get_logger
from app.utils.constants import MAX_WINNER_COUNT

logger = get_logger(__name__)


class TestLotteryService(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.table_name = "winners_test_table"

    @patch("app.repositories.winner_repository.get_new_version", return_value=1)
    @patch("app.repositories.winner_repository.create_versioned_table", return_value="winners_test_table")
    @patch("app.repositories.winner_repository.get_winner_count")
    @patch("app.repositories.winner_repository.insert_winner")
    @patch("app.repositories.winner_repository.get_winners", return_value=[{"email": "test@example.com", "state": "CA"}])
    @patch("app.api.fetch_random_users.fetch_default_users", return_value=[{"email": "test@example.com", "address": {"state": "CA"}}])
    def test_process_winners(self, mock_fetch_users, mock_get_winners, mock_insert, mock_get_count, mock_create_table, mock_get_version):
        """Test the complete lottery process with proper winner count increments and validations."""
        mock_get_count.side_effect = [0] + [i for i in range(1, MAX_WINNER_COUNT)]

        # Ensure function calls are recorded
        mock_create_table.reset_mock()
        mock_fetch_users.reset_mock()
        mock_insert.reset_mock()
        mock_get_winners.reset_mock()

        winners = process_winners()

        # Ensure the number of winners is correct
        self.assertIsInstance(winners, list)
        self.assertEqual(len(winners), MAX_WINNER_COUNT, "The number of winners does not match the expected count.")

        # Ensure all states are unique
        states = [winner[1] for winner in winners]
        self.assertEqual(len(states), len(set(states)), "Duplicate states found among winners.")

        logger.info("Test for process_winners passed with full validation.")


if __name__ == "__main__":
    unittest.main()

