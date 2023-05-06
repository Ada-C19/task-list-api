from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body.get["title"]
        description = request_body.get["description"]
        completed_at = request_body.get["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    is_complete = True
    if not new_task.completed_at:
        is_complete = False 

    return jsonify("id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.completed_at), 201 

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    all_tasks = task.query.all() 
    for task in all_tasks: 
        response.append(task.to_dict())

    return jsonify(response), 200


@tasks_bp.route("/<tasks>", methods=["GET"])
def get_no_saved_tasks:
response = []
pass

@tasks_bp.route("/<tasks>", methods=["GET"])
def get_one_task(task_id):
    try: 
        tasks_id = int(task_id)
    except ValueError:
        return {"message": f"invalid id: {task_id}"}, 400
    
    task = Task.query.get(task_id)

    return task.to_dict(), 200

    

