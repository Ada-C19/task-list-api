from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


#POST request
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body.get("completed_at"))

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": not new_task.completed_at is None
        }
    }, 201

#POST request
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    #logi: ver si hay tasks:
    all_tasks = Task.query.all()
    
    if not all_tasks:
        return [], 200
    
    else:
        #returning a list of restarant objects
        for task in all_tasks:
            response.append(task.to_dict())

    return jsonify(response), 200
