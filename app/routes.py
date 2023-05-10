from app import db

from flask import Blueprint, jsonify, make_response, request

from app.models.task import Task

# DEFINING THE TASK BLUEPRINT
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# ============================= CRUD ROUTES =============================
# CREATE TASK- POST request to /tasks
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    # return make_response(f"Task {new_task.title} successfully created", 201)
    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": True if new_task.completed_at else False  
    }}, 201
    

# READ ALL TASKS- GET request to /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False 
        })
    return jsonify(tasks_response), 200


# READ ONE TASK- GET request to /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = Task.query.get(task_id)

    return { "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": True if task.completed_at else False
        }
    }, 200