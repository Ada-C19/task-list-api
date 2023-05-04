from flask import Blueprint
from app import db
from app.models.task import Task

task_api = Blueprint("task", __name__, url_prefix="/task")
