from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#creates one task
#FIXME: return correctly formatted output
#TODO: how to populate task id return object ??
@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(f"{new_task} has been created")), 201

#reads one task as long as at least one is saved
#FIXME: how to add the ID to attribute ??   
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at
            }
        )
    
    db.session.commit()

    return jsonify(tasks_response)
