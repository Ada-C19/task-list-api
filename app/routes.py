from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
# from os import abort


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_task_by_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"task {id} invalid"}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"message":f"task {id} not found"}, 404)) 
    
    return task
    

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }
    }, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            })
    return jsonify(tasks_response)


@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task_by_id(id)
    return {
        "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
    }, 200


@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task_by_id(id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    return {
        "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
    }, 200


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task_by_id(id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f"Task {id} \"{task.title}\" successfully deleted"
    }, 200