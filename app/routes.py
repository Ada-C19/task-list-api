from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
        new_task.completed_at = None
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.to_dict()}, 201

@tasks_bp.route("", methods=['GET'])
def handle_tasks():

    tasks = Task.query.all()
    tasks_response = [Task.to_dict(task) for task in tasks]
    return jsonify(tasks_response), 200

def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"Task {id} invalid"}, 400))

    item = model.query.get(id)

    return item if item else abort(make_response({"message":f"Task {id} not found"}, 404))

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = get_valid_item_by_id(Task, task_id)
    # may not need line below, has worked for others as it's already
    # returned in get_valid_item_by_id
    Task.query.get(task_id)

    return {"task":{
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": (task.completed_at != None)}}, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = get_valid_item_by_id(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.to_dict()},200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_valid_item_by_id(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}