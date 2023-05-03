from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods = ["GET"])
def get_tasks():
    response = []
    all_tasks = Task.query.all()
    for task in all_tasks:
        response.append(task.to_dict())
    return jsonify(response), 200

@task_bp.route("", methods = ["POST"])
def create_new_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
    )
    db.session.add(new_task)
    db.session.commit()

    result = new_task.to_dict()
    return {"task": new_task.to_dict()}, 201

@task_bp.route("/<task_id>", methods = ["GET"])
def get_task_by_id(task_id):
    task = validate_task(task_id)
    return {"task": task.to_dict()}, 200

def validate_task(task_id):
    try:
        valid_task_id = int(task_id)
    except:
        return abort(make_response({"message": f"invalid id: {task_id}"}, 400))
    
    return Task.query.get_or_404(valid_task_id)
