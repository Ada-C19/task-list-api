from flask import Blueprint, request, make_response
from .models.task import Task
from app import db

task_bp = Blueprint("task", __name__, url_prefix="/tasks")


# Create task:
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    task = Task.from_dict(request_body)
    db.session.add(task)
    db.session.commit()
    response = Task.query.all()
    response_body ={"task":{"id":response[0].task_id,
                            "title":request_body["title"],
                            "description":request_body["description"],
                            "is_complete": False}} #request_body["completed_at"]
    return make_response(response_body, 201)

