from flask import Blueprint, request, jsonify, abort, make_response
from app.models.task import Task
from app import db

# Define all routes with tasks_bp start with url_prefix (/tasks)
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# @blueprint_name.route("/endpoint/path/here", methods=["GET"])
# def endpoint_name():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"msg": f"Invalid id '{task_id}'"}, 400))
    task = Task.query.get(task_id)
    return task if task else abort(make_response({"msg": f"Na task with task id '{task_id}'"}, 404))
        
@tasks_bp.route("", methods=["POST"])
def create_a_task():
    
    request_body = request.get_json()
    
    try:
        new_task = Task(title=request_body["title"], description=request_body["description"])
    except KeyError:
        return {
            "details": "Invalid data"
        }, 400
    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task": new_task.to_dict()
    }, 201
    
@tasks_bp.route("", methods=["GET"])
def get_saved_tasks():
    tasks = Task.query.all()
    task_response = []
    # Question: Isn't query.all() return result as a list already? why append again?
    if tasks is not None:
        for task in tasks:
    # Question: will this work without to_dict()?
            task_response.append(task.to_dict())
        return jsonify(task_response), 200
    else:
        return tasks, 200
    
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return {
        "task": task.to_dict()
    }, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    task = validate_task(task_id)
    if "title" in request_body:
        task.title = request_body["title"]
    if "description" in request_body:
        task.description = request_body["description"]
    #TODO:Update the completed_at attribute
    db.session.commit()
    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = validate_task(task_id)
    
    db.session.delete(task_to_delete)
    db.session.commit()
    
    return {
        "details": f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'
    }, 200