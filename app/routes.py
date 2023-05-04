from flask import Blueprint, jsonify, abort, make_response, request
from os import abort
from app import db
from app.models.task import Task

task_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try: 
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task: 
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task 

@task_bp.route("", methods=['GET'])
def read_all_books():
    task_response = []
    tasks = Task.query.all()
    for task in tasks:
        task_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description, 
            "completed_at": task.completed_at
        })
    return jsonify(task_response)

