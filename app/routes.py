from flask import Blueprint, jsonify
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# get all endpoint
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    tasks = Task.query.all()

    task_list = [task.to_dict() for task in tasks]

    return jsonify(task_list), 200
