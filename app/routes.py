from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# # Route to create a task
# @tasks_bp.route("", methods=["POST"])

# def create_task():
#     request_body = request.get_json()
    
#     new_task = Task(
#         title=request_body["title"],
#         description=request_body["description"]
#     )

# Route to get tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })

    return jsonify(tasks_response), 200


# Validate ID function
def validate_id(task_id):
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response({"message": f"Task with ID {task_id} not found."}, 404))

    return task

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):

    task = validate_id(task_id)

    return {"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}, 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    pass