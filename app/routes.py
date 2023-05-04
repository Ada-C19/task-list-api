from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# route for posting a task to db
@task_bp.route("", methods=['POST'])
def post_one_task():
    request_body = request.get_json()
    new_task = Task(title=request_body['title'],
                    description=request_body['description'],
                    completed_at=None)
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "completed_at": new_task.completed_at
            }
        }), 201
