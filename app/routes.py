from flask import Blueprint, jsonify, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("read_all_tasks", __name__, url_prefix=("/tasks"))

# create route (get) to get all tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
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


# create a task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task(
        title = request_body.get["title"],
        description = request_body.get["description"],
        completed_at = request_body.get["completed_at"]
        )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at != None
        }
    }), 201
    

# get a specific task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_specific_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at != None
        }
    })
    


# update a task
@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    request_body = request.get_json()
    
    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)
    
    db.session.commit()
    
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at != None
        }
    })
    
# detele a task 
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    })
