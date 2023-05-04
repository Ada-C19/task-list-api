from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201




