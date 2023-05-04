from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv
import os

#create instances
db = SQLAlchemy()
migrate = Migrate()

load_dotenv()


def create_app(testing=None):
    app = Flask(__name__)



    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if testing is None:

        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")

    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_TEST")

    app.config["DEBUG"] = True

    from app.models import Task
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import task_api
    app.register_blueprint(task_api)

    return app
