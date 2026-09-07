from flask import Flask
from dotenv import load_dotenv


def create_app(config_name=None):
    """Flask application factory."""
    load_dotenv()
    app = Flask(__name__)

    if config_name:
        app.config.from_object(f"app.config.{config_name}")
    else:
        from app.config import Config
        app.config.from_object(Config)

    register_blueprints(app)
    register_error_handlers(app)

    return app


def register_blueprints(app):
    from app.routes.ask_routes import ask_bp
    app.register_blueprint(ask_bp)


def register_error_handlers(app):
    from app.utils.errors import register_error_handlers
    register_error_handlers(app)
