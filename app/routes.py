from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    results = [task.to_dict() for task in tasks]

    return jsonify(results)

# @tasks_bp.route("/<task_id>", methods=["GET"])
# def get_one_task():
#     tasks = Task.query.all()
#     results = [task.to_dict() for task in tasks]

#     return jsonify(results)