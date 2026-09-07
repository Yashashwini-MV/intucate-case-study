import asyncio

from flask import Blueprint, jsonify, request

from app.services import prompt_service, openai_service, history_service, batch_service
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


@ask_bp.route("/ask/batch", methods=["POST"])
def ask_batch():
    if not request.is_json:
        return jsonify({"error": "Request must contain JSON"}), 400

    data = request.get_json()

    if "userInputs" not in data:
        return jsonify({"error": "Missing required field: userInputs"}), 400

    user_inputs = data["userInputs"]

    if not isinstance(user_inputs, list):
        return jsonify({"error": "userInputs must be a list"}), 400

    if len(user_inputs) == 0:
        return jsonify({"error": "userInputs must not be empty"}), 400

    cleaned = []
    for i, item in enumerate(user_inputs):
        if not isinstance(item, str):
            return jsonify({"error": f"userInputs[{i}] must be a string"}), 400
        if not item.strip():
            return jsonify({"error": f"userInputs[{i}] must not be empty"}), 400
        cleaned.append(item.strip())

    try:
        responses = asyncio.run(batch_service.process_batch(cleaned))
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code

    return jsonify({"responses": responses}), 200
