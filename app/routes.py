from flask import Blueprint, jsonify, request, Response, abort, make_response
from app.models.task import Task
from app import db 


# create blueprint 
task_bp = Blueprint("task", __name__, url_prefix="/tasks")


# Create Task Route
@task_bp.route("", methods=["POST"])
def add_task(): 
    response_body = request.get_json()

    # TODO - from_dict method
    try:
        new_task = Task(title=response_body["title"], 
                        description=response_body["description"], 
                        )
    except KeyError: 
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_result()}, 201


# Get All Tasks Route
@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    all_tasks = Task.query.all()

    for task in all_tasks: 
        response.append(task.to_result())
    
    return jsonify(response), 200

# Get One Task Route
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id): 
    task = validate_item(Task, task_id)

    return {"task": task.to_result()}, 200

# Update a Task Route
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task, task_id)

    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()

    return {"task": task.to_result()}, 200

# Delete a Task Route 
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200

# VALIDATION HELPER FUNCTION
def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    item = model.query.get(item_id)
    
    if not item: 
        return abort(make_response({"message": f"Task {item_id} not found"}, 404))
    
    return item