from flask import Flask
from flask_session import Session
from app.config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config.from_pyfile('config.py')

    Session(app)

    with app.app_context():
        from . import routes
        return app
