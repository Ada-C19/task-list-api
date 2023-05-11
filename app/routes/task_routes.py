from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app.helper_functions import slack_mark_complete, validate_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# POST route for creating a task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":new_task.to_json()}), 201

# GET route for reading all tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)

    description_query = request.args.get("description")
    if description_query:
        tasks = Task.query.filter_by(description=description_query)
    
    completed_query = request.args.get("is_complete")
    if completed_query:
        tasks = Task.query.filter_by(is_completed = completed_query)

    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()

    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
        # tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()
        

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200

#GET route to read one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task,task_id)
    return jsonify({"task": task.to_json()}), 200

#UPDATE route to edit a task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_json()}), 200

#DELETE existing task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"})

#PATCH REQUEST marking a test complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_complete_status(task_id):
    task_completed = validate_model(Task, task_id)
    
    request_body = request.get_json()
    
    task_completed.mark_complete(request_body)
    
    db.session.commit()

    slack_mark_complete(task_completed)

    return jsonify({"task":task_completed.to_json()}), 200 


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_incomplete_status(task_id):
    task_to_update = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task_to_update.mark_incomplete(request_body)

    db.session.commit()
    return jsonify({"task":task_to_update.to_json()}), 200

