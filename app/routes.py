from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

# wave 1 routes
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title = request_body["title"],
                        description = request_body["description"])
        
        db.session.add(new_task)
        db.session.commit()

        message  = {
            "task": new_task.to_dict()
        }
        return make_response(message, 201)
    except KeyError as e:
        abort(make_response({"details": "Invalid data"}, 400))

@task_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    message  = {
            "task": task.to_dict()
        }

    return make_response(message, 200)
    
# validate helper function
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    tasks = Task.query.all()
    for task in tasks:
        if task.task_id == task_id:
            return task
    
    abort(make_response({"message":f"task {task_id} not found"}, 404))

@task_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    
    db.session.delete(task)
    db.session.commit()

    message  = {
            "task": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }

    return make_response(message, 200)
