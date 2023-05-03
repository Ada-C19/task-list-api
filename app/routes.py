from flask import Blueprint, request
from app.models.task import Task

# Define all routes with tasks_bp start with url_prefix (/tasks)
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# @blueprint_name.route("/endpoint/path/here", methods=["GET"])
# def endpoint_name():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body

@tasks_bp.route("", methods=["POST"])
def create_a_task():
    
    
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
    return request_body