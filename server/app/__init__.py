from flask import Flask
from flask_mongoengine import MongoEngine
from settings import config
from flask_cors import CORS

db = MongoEngine()


def create_app():
    # initalize instance of Flask application
    app = Flask(__name__)

    # import configuration settings into Flask application instance
    app.config.from_object(config)
    config.init_app(app)

    CORS(app, supports_credentials=True)

    # initialize connection to MongoDB
    db.init_app(app)

    from .admin import create_admin_console
    create_admin_console(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
