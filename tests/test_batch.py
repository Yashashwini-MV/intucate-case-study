import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio

from app import create_app
from app.utils.errors import AppError


@pytest.fixture
def client():
    app = create_app("TestingConfig")
    with app.test_client() as client:
        yield client


class TestBatchValidRequest:
    @patch("app.services.batch_service.history_service")
    @patch("app.services.batch_service.openai_service")
    @patch("app.services.batch_service.prompt_service")
    def test_returns_200_with_responses(self, mock_prompt, mock_openai, mock_history, client):
        mock_prompt.build_prompt.side_effect = lambda x: f"prompt for {x}"
        mock_openai.get_chat_response_async = AsyncMock(side_effect=lambda x: f"answer for {x.split('for ')[1]}")

        response = client.post("/ask/batch", json={"userInputs": ["A", "B", "C"]})

        assert response.status_code == 200
        data = response.get_json()
        assert "responses" in data
        assert len(data["responses"]) == 3

    @patch("app.services.batch_service.history_service")
    @patch("app.services.batch_service.openai_service")
    @patch("app.services.batch_service.prompt_service")
    def test_preserves_input_order(self, mock_prompt, mock_openai, mock_history, client):
        call_order = []

        async def fake_async(prompt):
            idx = prompt.split("for ")[1]
            call_order.append(idx)
            return f"response {idx}"

        mock_prompt.build_prompt.side_effect = lambda x: f"prompt for {x}"
        mock_openai.get_chat_response_async = AsyncMock(side_effect=fake_async)

        response = client.post("/ask/batch", json={"userInputs": ["C", "A", "B"]})

        data = response.get_json()
        assert data["responses"] == ["response C", "response A", "response B"]

    @patch("app.services.batch_service.history_service")
    @patch("app.services.batch_service.openai_service")
    @patch("app.services.batch_service.prompt_service")
    def test_saves_history_for_each_item(self, mock_prompt, mock_openai, mock_history, client):
        mock_prompt.build_prompt.side_effect = lambda x: f"prompt for {x}"
        mock_openai.get_chat_response_async = AsyncMock(side_effect=lambda x: f"answer for {x.split('for ')[1]}")

        client.post("/ask/batch", json={"userInputs": ["X", "Y"]})

        assert mock_history.save_history.call_count == 2
        mock_history.save_history.assert_any_call("X", "answer for X")
        mock_history.save_history.assert_any_call("Y", "answer for Y")


class TestBatchConcurrency:
    @patch("app.services.batch_service.history_service")
    @patch("app.services.batch_service.openai_service")
    @patch("app.services.batch_service.prompt_service")
    def test_items_run_concurrently(self, mock_prompt, mock_openai, mock_history, client):
        started = []
        finished = []

        async def slow_async(prompt):
            item = prompt.split("for ")[1]
            started.append(item)
            await asyncio.sleep(0.05)
            finished.append(item)
            return f"response {item}"

        mock_prompt.build_prompt.side_effect = lambda x: f"prompt for {x}"
        mock_openai.get_chat_response_async = AsyncMock(side_effect=slow_async)

        response = client.post("/ask/batch", json={"userInputs": ["A", "B", "C"]})

        assert response.status_code == 200
        assert len(started) == 3
        assert len(finished) == 3
        data = response.get_json()
        assert data["responses"] == ["response A", "response B", "response C"]


class TestBatchMissingJson:
    def test_returns_400_when_no_json(self, client):
        response = client.post("/ask/batch", content_type="text/plain", data="not json")

        assert response.status_code == 400
        assert "JSON" in response.get_json()["error"]

    def test_returns_400_when_empty_body(self, client):
        response = client.post("/ask/batch", content_type="application/json", data="")

        assert response.status_code == 400


class TestBatchMissingUserInputs:
    def test_returns_400_when_user_inputs_missing(self, client):
        response = client.post("/ask/batch", json={})

        assert response.status_code == 400
        assert "userInputs" in response.get_json()["error"]

    def test_returns_400_when_other_field_provided(self, client):
        response = client.post("/ask/batch", json={"inputs": ["a"]})

        assert response.status_code == 400


class TestBatchInvalidUserInputs:
    def test_returns_400_when_not_a_list(self, client):
        response = client.post("/ask/batch", json={"userInputs": "not a list"})

        assert response.status_code == 400
        assert "list" in response.get_json()["error"].lower()

    def test_returns_400_when_empty_list(self, client):
        response = client.post("/ask/batch", json={"userInputs": []})

        assert response.status_code == 400
        assert "empty" in response.get_json()["error"].lower()

    def test_returns_400_when_item_not_string(self, client):
        response = client.post("/ask/batch", json={"userInputs": ["a", 123, "c"]})

        assert response.status_code == 400
        assert "string" in response.get_json()["error"].lower()

    def test_returns_400_when_item_is_none(self, client):
        response = client.post("/ask/batch", json={"userInputs": [None]})

        assert response.status_code == 400

    def test_returns_400_when_item_empty_string(self, client):
        response = client.post("/ask/batch", json={"userInputs": ["a", "", "c"]})

        assert response.status_code == 400
        assert "empty" in response.get_json()["error"].lower()

    def test_returns_400_when_item_whitespace_only(self, client):
        response = client.post("/ask/batch", json={"userInputs": ["a", "   ", "c"]})

        assert response.status_code == 400
        assert "empty" in response.get_json()["error"].lower()

    def test_error_message_includes_item_index(self, client):
        response = client.post("/ask/batch", json={"userInputs": ["a", 1, "c"]})

        assert response.status_code == 400
        assert "[1]" in response.get_json()["error"]


class TestBatchOpenAIFailure:
    @patch("app.services.batch_service.openai_service")
    @patch("app.services.batch_service.prompt_service")
    def test_returns_502_when_openai_fails(self, mock_prompt, mock_openai, client):
        mock_prompt.build_prompt.return_value = "prompt"
        mock_openai.get_chat_response_async = AsyncMock(
            side_effect=AppError("Failed to get response from OpenAI", status_code=502)
        )

        response = client.post("/ask/batch", json={"userInputs": ["test"]})

        assert response.status_code == 502
        assert "OpenAI" in response.get_json()["error"]


class TestBatchPromptServiceFailure:
    @patch("app.services.batch_service.prompt_service")
    def test_returns_500_when_prompt_not_found(self, mock_prompt, client):
        mock_prompt.build_prompt.side_effect = AppError("Education_Prompt not found", status_code=500)

        response = client.post("/ask/batch", json={"userInputs": ["test"]})

        assert response.status_code == 500
        assert "Education_Prompt not found" in response.get_json()["error"]
