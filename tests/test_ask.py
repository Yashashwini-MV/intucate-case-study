import pytest
from unittest.mock import patch
from app import create_app


@pytest.fixture
def client():
    app = create_app("TestingConfig")
    with app.test_client() as client:
        yield client


EDUCATION_TEMPLATE = "You are an expert in education domain. Answer the following: {{userInput}}"


class TestAskValidRequest:
    @patch("app.routes.ask_routes.prompt_service")
    def test_returns_200_with_prompt(self, mock_service, client):
        mock_service.build_prompt.return_value = "You are an expert in education domain. Answer the following: What is photosynthesis?"

        response = client.post("/ask", json={"userInput": "What is photosynthesis?"})

        assert response.status_code == 200
        data = response.get_json()
        assert "prompt" in data
        assert "What is photosynthesis?" in data["prompt"]

    @patch("app.routes.ask_routes.prompt_service")
    def test_passes_user_input_to_service(self, mock_service, client):
        mock_service.build_prompt.return_value = "final prompt"

        client.post("/ask", json={"userInput": "test input"})

        mock_service.build_prompt.assert_called_once_with("test input")


class TestAskMissingJson:
    def test_returns_400_when_no_json(self, client):
        response = client.post("/ask", content_type="text/plain", data="not json")

        assert response.status_code == 400
        assert "JSON" in response.get_json()["error"]

    def test_returns_400_when_empty_body(self, client):
        response = client.post("/ask", content_type="application/json", data="")

        assert response.status_code == 400


class TestAskMissingUserInput:
    def test_returns_400_when_user_input_missing(self, client):
        response = client.post("/ask", json={})

        assert response.status_code == 400
        assert "userInput" in response.get_json()["error"]

    def test_returns_400_when_other_field_provided(self, client):
        response = client.post("/ask", json={"question": "hello"})

        assert response.status_code == 400


class TestAskInvalidUserInput:
    def test_returns_400_when_user_input_not_string(self, client):
        response = client.post("/ask", json={"userInput": 123})

        assert response.status_code == 400
        assert "string" in response.get_json()["error"].lower()

    def test_returns_400_when_user_input_is_list(self, client):
        response = client.post("/ask", json={"userInput": ["a", "b"]})

        assert response.status_code == 400

    def test_returns_400_when_user_input_is_bool(self, client):
        response = client.post("/ask", json={"userInput": True})

        assert response.status_code == 400


class TestAskEmptyUserInput:
    def test_returns_400_when_empty_string(self, client):
        response = client.post("/ask", json={"userInput": ""})

        assert response.status_code == 400
        assert "empty" in response.get_json()["error"].lower()

    def test_returns_400_when_whitespace_only(self, client):
        response = client.post("/ask", json={"userInput": "   "})

        assert response.status_code == 400
        assert "empty" in response.get_json()["error"].lower()

    def test_returns_400_when_tabs_only(self, client):
        response = client.post("/ask", json={"userInput": "\t\t"})

        assert response.status_code == 400


class TestAskServiceError:
    @patch("app.routes.ask_routes.prompt_service")
    def test_returns_500_when_prompt_not_found(self, mock_service, client):
        from app.utils.errors import AppError
        mock_service.build_prompt.side_effect = AppError("Education_Prompt not found", status_code=500)

        response = client.post("/ask", json={"userInput": "test"})

        assert response.status_code == 500
        assert "Education_Prompt not found" in response.get_json()["error"]
