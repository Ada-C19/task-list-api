from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"Task {id} is invalid"}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"message": f"Task {id} not found"}, 404))

    return task

@tasks_bp.route("", methods=["POST"])
def create_task():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = None
    )
    
    db.session.add(new_task)
    db.session.commit()
    task_dict = dict(task=new_task.to_dict())
    
    return make_response(jsonify(task_dict), 201)
    


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    tasks_list = []
    for task in tasks:
        tasks_list.append(task.to_dict())
    return jsonify(tasks_list)

@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    tasks = validate_task(id)
    task_dict = dict(task=tasks.to_dict())
    
    # return task_dict
    return make_response(jsonify(task_dict), 200)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)
    task_data = request.get_json()
    
    task.title = task_data["title"]
    task.description = task_data["description"]
    
    db.session.commit()
    
    task_dict = dict(task=task.to_dict())
    return make_response(jsonify(task_dict), 200)

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task = validate_task(id)
    
    deleted_response = {
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }
    
    db.session.delete(task)
    db.session.commit()
    
    return make_response(jsonify(deleted_response), 200)