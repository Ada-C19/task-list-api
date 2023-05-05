from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

#CREATE
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    #create a new instance of Task
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body.get("completed_at", None)
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.task_display_dict()), 201


#GET ALL TASKS

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []   
    #to extract data from the database not from the task obj - REMINDER
    tasks = Task.query.all()

    response = [each_task.task_display_dict() for each_task in tasks]

    return jsonify(response), 200

