from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__,url_prefix="/tasks")


@task_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"], description = request_body["description"], completed_at = request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify(f"Task {new_task.title} successfully created", 201))

@task_bp.route('', methods=['GET'])
def get_all_tasks():
    task_response = []
    tasks = Task.query.all()
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response)
    