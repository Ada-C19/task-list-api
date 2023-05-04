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
            "completed_at": bool(new_task.completed_at)
            }
        }), 201

# Get all tasks
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "completed_at": bool(task.completed_at)
        })
    return jsonify(tasks_response), 200

# get one saved task
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get(task_id)
    response_body = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "completed_at": task.completed_at
        }
    }
    return jsonify(response_body), 200


# update task route
@task_bp.route("/<task_id>", methods=["PUT"])
def update_route_by_id(task_id):
    request_body = request.get_json()
    task = Task.query.get(task_id)
    task_response = {
        "task": {
            "title": request_body['title'],
            "description": request_body['description'],
            'id': task.task_id,
            'completed_at': bool(task.completed_at)
            }
        }
    return jsonify(task_response), 200