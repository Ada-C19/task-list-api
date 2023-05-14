from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request


task_list_bp = Blueprint("task_list", __name__, url_prefix="/tasks")


# create
@task_list_bp.route("", methods=["POST"])

def post_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid request", 400)
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit() 
    
    return make_response(f"New task: {new_task.title},  created", 201)

# if not completed_at:
#         return make_response({
#             "task": {"id": new_task.id,
#             "title": new_task.title,
#             "description": new.task.description,
#             "is_complete": false}
#   }, 201
#         )









# #read
# @task_list_bp.route("/tasks", methods=["GET"])


# #update

# # delete


