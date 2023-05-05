from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy import asc, desc


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#validation helper function
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task


#POST request
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not request_body.get("description") or not request_body.get("title"):
            abort(make_response({
                    "details": "Invalid data"
                }, 400))

    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body.get("completed_at"))

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": not new_task.completed_at is None
        }
    }, 201

#Get all request
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    sort_order = request.args.get("sort")
    all_tasks = Task.query.all()
    if not all_tasks:
        return jsonify(response), 200
    elif not sort_order:
            all_tasks = Task.query.all()
    elif all_tasks and sort_order == "asc":
            all_tasks = Task.query.order_by(asc(Task.title)).all()
    elif all_tasks and sort_order == "desc":
            all_tasks = Task.query.order_by(desc(Task.title)).all()
        
    for task in all_tasks:
        response.append(task.to_dict())

    return jsonify(response), 200


#older version:
# response = []

#   all_tasks = Task.query.all()

#    if not all_tasks:
#         return jsonify(response), 200
#     else:
#         for task in all_tasks:
#             response.append(task.to_dict())

#     return jsonify(response), 200


#Get one task by id:
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = validate_task(task_id)
    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": not task.completed_at is None
        }
    }

#Update task by id
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task_by_id(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": not task.completed_at is None
        }
    }, 200

#Delete task 
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }
