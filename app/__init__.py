from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    
    if not test_config:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DEV_DB_URI")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "TEST_DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here

    return app
