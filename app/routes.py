from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from app import db
from datetime import date

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# CREATE TASK ENDPOINT
@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("description") or not request_body.get("completed_at"):
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body.get("completed_at"))
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": response_body(new_task)}), 201)

# GET TASKS ENDPOINT
@tasks_bp.route("", methods=["GET"])
def read_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif not sort_query:
        tasks = Task.query.all()
    
    tasks_response = []

    for task in tasks:
        tasks_response.append(response_body(task))

    return jsonify(tasks_response)

# GET ONE TASK ENDPOINT
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)

    return {"task": response_body(task)}

# UPDATE TASK ENDPOINT
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    request_body = request.get_json()

    task = validate_task(task_id)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": response_body(task)}

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = date.today()

    db.session.commit()

    return {"task": response_body_complete(task)}

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    
    db.session.commit()

    return {"task": response_body(task)}

# DELETE TASK ENDPOINT
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"})


# HELPER FUNCTIONS
def response_body(task):
    return {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }

def response_body_complete(task):
    return {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
        }

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task