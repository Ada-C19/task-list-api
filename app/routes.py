from flask import Blueprint
from app import db
from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods = ["GET"])
def get_all_tasks():
    response_body = "All the tasks!"
    return response_body, 200
