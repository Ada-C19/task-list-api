from flask import Blueprint
from app import db

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Route to get tasks
@task_bp.route("", methods=["GET"])

def read_all_tasks():
    tasks_response = []

    tasks = Task.query.all()

    for task in tasks:
        tasks_reponse.append({
            "title": task.title,
            "description": task.description,
        })

    return tasks_response