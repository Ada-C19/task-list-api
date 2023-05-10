from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from app.helper import validate_id

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#get all tasks-"/tasks"-GET(read)
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200


#get one tasks-"/tasks/1"-GET(read)
@tasks_bp.route("/<id>", methods=["GET"])
def get_task(id):
    task = validate_id(id)
    return jsonify({"task":task.to_dict()}), 200
