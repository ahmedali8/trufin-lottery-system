import unittest
from unittest.mock import patch, MagicMock
from app.services.lottery_service import process_winners
from app.repositories.winner_repository import (
    create_versioned_table, insert_winner, get_winner_count, get_winners, get_new_version
)
from app.api.fetch_random_users import fetch_default_users
from app.utils.logger import log_info
from app.utils.constants import MAX_WINNER_COUNT

class TestLotterySystem(unittest.TestCase):

    @patch("app.repositories.winner_repository.get_new_version", return_value=1)
    @patch("app.repositories.winner_repository.create_versioned_table", return_value="winner_20250212_142716_v1")
    @patch("app.repositories.winner_repository.get_winner_count", side_effect=[0, MAX_WINNER_COUNT])
    @patch("app.repositories.winner_repository.insert_winner")
    @patch("app.repositories.winner_repository.get_winners", return_value=[{"email": "eldon.swift@email.com", "state": "Wisconsin"}])
    @patch("app.api.fetch_random_users.fetch_default_users", return_value=[{"email": "eldon.swift@email.com", "address": {"state": "Wisconsin"}}])
    def test_process_winners(self, mock_fetch_users, mock_get_winners, mock_insert, mock_get_count, mock_create_table, mock_get_version):
        """Test the full lottery process"""
        process_winners()

        # Ensure table creation
        mock_create_table.assert_called_once_with(1)

        # Ensure fetch users is called at least once
        mock_fetch_users.assert_called()

        # Ensure winner is inserted
        mock_insert.assert_called()

        # Ensure final winners are retrieved
        mock_get_winners.assert_called()

        log_info("Test for process_winners passed.")


if __name__ == "__main__":
    unittest.main()

