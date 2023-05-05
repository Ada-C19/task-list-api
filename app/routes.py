from flask import Blueprint, jsonify, abort, make_response, request
from os import abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try: 
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task: 
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task 

@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    print("******MY PRINT******",request_body.get("description"))
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    )

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": True if new_task.completed_at else False
        }
    }, 201

@tasks_bp.route("", methods=['GET'])
def read_all_tasks():
    task_response = []
    tasks = Task.query.all()
    for task in tasks:
        task_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description, 
            "is_complete": True if task.completed_at else False
        })
    return jsonify(task_response), 200



