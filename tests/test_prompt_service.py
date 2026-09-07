from unittest.mock import patch
import pytest

from app.services import prompt_service
from app.utils.errors import AppError


EDUCATION_TEMPLATE = "You are an expert in education domain. Answer the following: {{userInput}}"


class TestBuildPrompt:
    @patch("app.services.prompt_service.prompt_repository")
    def test_replaces_placeholder_with_user_input(self, mock_repo):
        mock_repo.get_prompt_by_id.return_value = {
            "_id": "Education_Prompt",
            "template": EDUCATION_TEMPLATE,
        }

        result = prompt_service.build_prompt("What is photosynthesis?")

        mock_repo.get_prompt_by_id.assert_called_once_with("Education_Prompt")
        assert result == "You are an expert in education domain. Answer the following: What is photosynthesis?"

    @patch("app.services.prompt_service.prompt_repository")
    def test_preserves_punctuation_and_special_characters(self, mock_repo):
        mock_repo.get_prompt_by_id.return_value = {
            "_id": "Education_Prompt",
            "template": EDUCATION_TEMPLATE,
        }

        user_input = "Hello! How are you? I'm fine — thanks."
        result = prompt_service.build_prompt(user_input)

        assert "Hello! How are you? I'm fine — thanks." in result

    @patch("app.services.prompt_service.prompt_repository")
    def test_raises_error_when_prompt_not_found(self, mock_repo):
        mock_repo.get_prompt_by_id.return_value = None

        with pytest.raises(AppError) as exc_info:
            prompt_service.build_prompt("test")

        assert exc_info.value.status_code == 500
        assert "Education_Prompt not found" in exc_info.value.message

    @patch("app.services.prompt_service.prompt_repository")
    def test_returns_prompt_with_placeholder_replaced(self, mock_repo):
        mock_repo.get_prompt_by_id.return_value = {
            "_id": "Education_Prompt",
            "template": "Explain: {{userInput}}",
        }

        result = prompt_service.build_prompt("gravity")

        assert result == "Explain: gravity"
        assert "{{userInput}}" not in result
