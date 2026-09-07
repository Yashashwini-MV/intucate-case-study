from unittest.mock import patch

from app.services import history_service


class TestSaveHistory:
    @patch("app.services.history_service.history_repository")
    def test_calls_insert_history_with_correct_args(self, mock_repo):
        mock_repo.insert_history.return_value = "inserted_id"

        result = history_service.save_history("user question", "ai response")

        mock_repo.insert_history.assert_called_once_with("user question", "ai response")
        assert result == "inserted_id"
