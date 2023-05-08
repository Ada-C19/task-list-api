from flask import Blueprint, request, jsonify
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    print(request_body)
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {
        "task":{
            "id":new_task.task_id,
            "title":new_task.title,
            "description":new_task.description,
            "is_complete": False
        }
    }, 201

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    #Retrieve a list of all the task objects in database
    all_tasks = Task.query.all()
    
    tasks_response = []
    for task in all_tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200

@tasks_bp.route("<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)

    return {
        "task": task.to_dict()
    }