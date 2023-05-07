from flask import Blueprint, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    print(request_body)
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {
        "task":{
            "id":new_task.task_id,
            "title":new_task.title,
            "description":new_task.description,
            "is_complete": False
        }
    }, 201
