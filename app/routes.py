from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)