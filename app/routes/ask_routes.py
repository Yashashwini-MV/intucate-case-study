from flask import Blueprint, jsonify, request

from app.services import prompt_service, openai_service, history_service
from app.utils.errors import AppError

ask_bp = Blueprint("ask", __name__)


@ask_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@ask_bp.route("/ask", methods=["POST"])
def ask():
    if not request.is_json:
        return jsonify({"error": "Request must contain JSON"}), 400

    data = request.get_json()

    if "userInput" not in data:
        return jsonify({"error": "Missing required field: userInput"}), 400

    user_input = data["userInput"]

    if not isinstance(user_input, str):
        return jsonify({"error": "userInput must be a string"}), 400

    if not user_input.strip():
        return jsonify({"error": "userInput must not be empty"}), 400

    try:
        prompt = prompt_service.build_prompt(user_input.strip())
        response_text = openai_service.get_chat_response(prompt)
        history_service.save_history(user_input.strip(), response_text)
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({"response": response_text}), 200
