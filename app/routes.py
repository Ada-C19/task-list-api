from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    
    task = Task.query.get(task_id)
    
    return task if task else abort(make_response({'msg': f"No task with id {task_id}"}, 404))


@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=None)
    except KeyError:
        return {
            "details": "Invalid data"
            }, 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@tasks_bp.route("", methods=['GET'])
def handle_tasks():
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()
    
    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=['GET'])
def handle_task(task_id):
    task = validate_task(task_id)
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_one_task(task_id):
    request_body = request.get_json()

    task_to_update = validate_task(task_id)

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return {"task": task_to_update.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = validate_task(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return {
        "details": 
            f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'
        }, 200