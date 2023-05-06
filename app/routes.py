from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
# Helper Function
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({'message': f'Invalid Task id {task_id}'}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({'message': f'Task id {task_id} not found'}, 404))

    return task

# route for posting a task to db
@task_bp.route("", methods=['POST'])
def post_one_task():
    request_body = request.get_json()
    if not request_body.get('title') or not request_body.get('description'):
        return jsonify({"details": "Invalid data"}), 400
    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

# Get all tasks
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

# get one saved task
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    response_body = {
        "task": task.to_dict()
    }
    return jsonify(response_body), 200


# update task route
@task_bp.route("/<task_id>", methods=["PUT"])
def update_route_by_id(task_id):
    # Get the task and new data
    request_body = request.get_json()
    task = validate_task(task_id)

    # Save new Data
    task.title = request_body['title']
    task.description = request_body['description']
    db.session.commit()
    
    # Send back response
    task_response = {
        "task": task.to_dict()}
    return jsonify(task_response), 200

# Delete task
@task_bp.route("/<task_id>", methods=['DELETE'])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response_body = {"details": f'Task {task_id} "{task.title}" successfully deleted'}
    return jsonify(response_body), 200