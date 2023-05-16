from flask import Blueprint, make_response
from flask.json import jsonify
# from app import db
from app.models.task import Task

tasks_bp = Blueprint("read_all_tasks", __name__, url_prefix=("/tasks"))

# create route (get) to read all tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    tasks = Task.query.all() 
    
    for task in tasks: 
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at != None
        })
        
    return jsonify(tasks_response)
