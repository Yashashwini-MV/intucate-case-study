from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

from app.repositories import history_repository


class TestInsertHistory:
    @patch("app.repositories.history_repository.get_db")
    def test_inserts_document_with_correct_fields(self, mock_get_db):
        mock_collection = MagicMock()
        mock_collection.insert_one.return_value = MagicMock(inserted_id="abc123")
        mock_get_db.return_value = {"history": mock_collection}

        result = history_repository.insert_history("What is gravity?", "Gravity is a force.")

        mock_collection.insert_one.assert_called_once()
        doc = mock_collection.insert_one.call_args[0][0]
        assert doc["userInput"] == "What is gravity?"
        assert doc["response"] == "Gravity is a force."
        assert isinstance(doc["createdAt"], datetime)
        assert doc["createdAt"].tzinfo == timezone.utc

    @patch("app.repositories.history_repository.get_db")
    def test_returns_inserted_id(self, mock_get_db):
        mock_collection = MagicMock()
        mock_collection.insert_one.return_value = MagicMock(inserted_id="xyz789")
        mock_get_db.return_value = {"history": mock_collection}

        result = history_repository.insert_history("input", "output")

        assert result == "xyz789"
