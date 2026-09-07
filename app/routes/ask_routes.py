from flask import Blueprint, jsonify

ask_bp = Blueprint("ask", __name__)


@ask_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200
