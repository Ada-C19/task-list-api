from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

# All routes for tasks start with "/tasks" URL prefix
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({'msg': f"Invalid id '{id}'"}, 400))

    item = model.query.get(id)

    return item if item else abort(make_response({'msg': f"No {model.__name__} with id {id}"}, 404))


@tasks_bp.route("", methods=["GET"])
def handle_get_tasks_request():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        is_complete = False
        if task.to_dict()["completed_at"]:
            is_complete = True

        task_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete
        })

    return jsonify(task_response), 200


@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    # Check whether task "is_complete"
    is_complete = False
    if new_task.to_dict()["completed_at"]:
        is_complete = True

    return {
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
        }
    }, 201


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_get_single_task(task_id):
    task = get_valid_item_by_id(Task, task_id)
    task_dict = task.to_dict()

    is_complete = False
    if task_dict["completed_at"]:
        is_complete = True

    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete
        }
    }, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {
            "details": "Invalid data"
        }, 400
    task_to_update = get_valid_item_by_id(Task, task_id)
    
    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    is_complete = False
    if task_to_update.to_dict()["completed_at"]:
        is_complete = True
    
    return {
        "task": {
            "id": task_to_update.id,
            "title": task_to_update.title,
            "description": task_to_update.description,
            "is_complete": is_complete
        }
    }, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = get_valid_item_by_id(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return {'details': f'Task {task_to_delete.id} "{task_to_delete.title}" successfully deleted'}, 200