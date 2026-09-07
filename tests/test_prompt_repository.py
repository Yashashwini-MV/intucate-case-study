from unittest.mock import patch, MagicMock
from app.repositories import prompt_repository


class TestGetPromptById:
    @patch("app.repositories.prompt_repository.get_db")
    def test_returns_prompt_when_found(self, mock_get_db):
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {
            "_id": "Education_Prompt",
            "template": "You are an expert in education domain. Answer the following: {{userInput}}",
        }
        mock_get_db.return_value = {"prompts": mock_collection}

        result = prompt_repository.get_prompt_by_id("Education_Prompt")

        assert result is not None
        assert result["_id"] == "Education_Prompt"
        mock_collection.find_one.assert_called_once_with({"_id": "Education_Prompt"})

    @patch("app.repositories.prompt_repository.get_db")
    def test_returns_none_when_not_found(self, mock_get_db):
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None
        mock_get_db.return_value = {"prompts": mock_collection}

        result = prompt_repository.get_prompt_by_id("nonexistent")

        assert result is None


class TestUpsertPrompt:
    @patch("app.repositories.prompt_repository.get_db")
    def test_upserts_prompt(self, mock_get_db):
        mock_collection = MagicMock()
        mock_collection.update_one.return_value = MagicMock(upserted_id="Education_Prompt")
        mock_get_db.return_value = {"prompts": mock_collection}

        result = prompt_repository.upsert_prompt(
            "Education_Prompt",
            "You are an expert in education domain. Answer the following: {{userInput}}",
        )

        mock_collection.update_one.assert_called_once_with(
            {"_id": "Education_Prompt"},
            {"$set": {"template": "You are an expert in education domain. Answer the following: {{userInput}}"}},
            upsert=True,
        )
        assert result.upserted_id == "Education_Prompt"
