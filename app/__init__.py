from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import requests


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

token = os.environ.get("SLACK_API_TOKEN")

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("RENDER_DATABASE_URI")
        # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        #     "SQLALCHEMY_DATABASE_URI")
    
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")
    
    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .task_routes import tasks_bp
    app.register_blueprint(tasks_bp)
    
    from .goal_routes import goal_bp
    app.register_blueprint(goal_bp)
    
    return app
