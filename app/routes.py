from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.task import Task


task_bp = Blueprint("task", __name__,url_prefix = "/tasks")

# create
@task_bp.route("", methods = ["POST"])
def get_task():
    response_body = request.get_json()
    if "title" not in response_body or "description" not in response_body:
        return jsonify({ "details": "Invalid data"}), 400
    
    new_task = Task(
        title = response_body["title"],
        description = response_body["description"],
        completed_at = response_body.get("completed_at", None)
    )
    db.session.add(new_task)
    db.session.commit() 

    return jsonify({"task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.completed_at is not None
    }
    }), 201





    