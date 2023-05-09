from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db 


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# helper function to validate_task
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task


# Routes/Endpoints below 

# create one task
@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], 
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)


# read/get all tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed_at": task.completed_at,
                "is_completed": False if task.completed_at == None else True
            }
        )
    return jsonify(tasks_response), 200 


# read/get one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed_at": task.completed_at,
            "is_completed": False if task.completed_at == None else True
        }), 200


# update one task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.id = request_body["id"]
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]
    task.is_completed = request_body["is_completed"]

    db.session.commit()

    return jsonify(make_response(f"Task #{task.id} successfully updated")), 200 


# delete one task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify(make_response(f"Task #{task.id} successfully deleted")), 200


