from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

token = os.environ.get('SLACK_TOKEN')

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

# client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "RENDER_DATABASE_URI")
        # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        #     "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")
    
    db.init_app(app)
    migrate.init_app(app, db)

    

    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal

    
    from app.routes.task_routes import tasks_bp
    from app.routes.goal_routes import goals_bp
    # Register Blueprints here
    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)

    # client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    return app

