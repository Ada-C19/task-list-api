from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task
from sqlalchemy import desc, asc

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Sort ascending or descending order
# ascending - sorted()
# descending - reverse_sorted()

# Route to get tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    query_sort = request.args.get("sort")
    
    if query_sort == "asc":
        tasks = db.session.query(Task).order_by(asc(Task.title)).all()
    elif query_sort == "desc":
        tasks = db.session.query(Task).order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response), 200


# Validate ID function
def validate_id(task_id):
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response({"message": f"Task with ID {task_id} not found."}, 404))

    return task

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):

    task = validate_id(task_id)

    return {"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}, 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try: 
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"]
        )  
    except:
        return {
            "details": "Invalid data"
        }, 400
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }}), 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(task_id)
    request_body = request.get_json()
    
    task.title =  request_body["title"],
    task.description = request_body["description"]
    
    db.session.commit()

    return jsonify({"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
    }, 200

@tasks_bp.route("/<task_id>", methods=["PATCH"])
def mark_completed(task_id):
    pass