from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    is_complete = True
    if not new_task.completed_at:
        is_complete = False
    

    return jsonify({"task":
                    {"id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": is_complete
            }}), 201

@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    all_tasks = Task.query.all()

    for task in all_tasks:
        response.append(task.to_dict())

    return jsonify(response), 200 


# @task_bp.route("/<task_id>", methods=["GET"])
# def get_one_task(task_id):
    

# @task_bp.route("/<task_id>", methods="PUT")
# def update_task(task_id):
#     pass

# @task_bp.route("/<task_id>", methods=["DELETE"])
# def delete_task(task_id):
#     pass

# def validate_task(task_id):
#     try:
#         # some task var = int(task_id)
#         some_id = int(task_id)
#     except ValueError:
#         return abort(make_response({"msg": f"invalid id: {task_id}"}, 400))
    
#     return Task.query.get_or_404(task_id)