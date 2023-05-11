from flask import Blueprint, request, make_response, jsonify, abort
from ..models.task import Task
from app import db
from datetime import datetime
from app.routes.helper import send_requsest_to_slack, validate_model

task_bp = Blueprint("task", __name__, url_prefix="/tasks")


# Read all tasks:
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("sort") 

    if title_query == "asc":
        task_objects = Task.query.order_by(Task.title) 
    elif title_query == "desc":
        task_objects = Task.query.order_by(Task.title.desc()) 
    else:
        task_objects = Task.query.all()
    task_list = [task.to_dict() for task in task_objects]
    return make_response(jsonify(task_list), 200)
 
# Read one task:
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task_object = validate_model(Task, task_id)
    return make_response({"task" : task_object.to_dict()}, 200)

# Create task:
@task_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body_dict = request.get_json()
        task_object = Task.from_dict(request_body_dict)
        db.session.add(task_object)
        db.session.commit()
        return make_response({"task" : task_object.to_dict()}, 201)
    except(KeyError):
        return make_response({"details": "Invalid data"}, 400)
    
# Replace a task
@task_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    task_object = validate_model(Task, task_id)
    task_request_body_dict = request.get_json()
    task_object.title = task_request_body_dict.get("title")
    task_object.description = task_request_body_dict.get("description")
    task_object.complete_at = task_request_body_dict.get("completed_at")
    db.session.commit()
    return make_response({"task" : task_object.to_dict()}, 200)

# Delete a task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    response_object = validate_model(Task, task_id)
    db.session.delete(response_object)
    db.session.commit()
    return make_response({
        'details': f'Task {response_object.task_id} "{response_object.title}" successfully deleted'}, 200)

# Update a task, mark complete
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_mark_complete(task_id):
    task_object = validate_model(Task, task_id)
    task_object.completed_at = datetime.utcnow()
    db.session.commit()
    response_text = f"Task #{task_object.title} is complete!"
    send_requsest_to_slack(response_text)
    return make_response({"task" : task_object.to_dict()}, 200)


# Update a task, mark incomplete
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_mark_incomplete(task_id):
    task_object = validate_model(Task, task_id)
    task_object.completed_at = None
    db.session.commit()
    response_text = f"Task #{task_object.title} is incomplete!"
    send_requsest_to_slack(response_text)
    return make_response({"task" : task_object.to_dict()}, 200)


