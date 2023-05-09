from flask import Blueprint, jsonify, abort, make_response, request
from datetime import date
from app import db
from app.models.task import Task
# from app.models.goal import Goal

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Sorry, task {task_id} does not exist"}, 404))

    return task

@task_bp.route("", methods=['POST'])

# define a route for creating a task
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
        )
    except:
        abort(make_response({"details": f"Invalid data"}, 400))

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

# define a route for getting all tasks
@task_bp.route("", methods=["GET"])
def read_all_tasks():
    # querries
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_at_query = request.args.get("completed_at")
    sort_query = request.args.get("sort")

    if title_query:
        tasks = Tasks.query.filter_by(title=title_query)
    
    elif description_query:
        tasks = Task.query.filter_by(description=description_query)
    
    elif completed_at_query:
        tasks = Task.query.filter_by(completed_at=completed_at_query)
    
    elif sort_query:
        if sort_query == 'asc':
            tasks = Task.query.order_by(Task.title).all()
        elif sort_query == 'desc':
            tasks = Task.query.order_by(Task.title.desc()).all()
    
    else:
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

@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        }
    }, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        }
    }, 200

# in progress
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def task_mark_complete(task_id):
    task = validate_task(task_id)

    request_body = request.get_json() 

    task.completed_at = date.today()

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        }
    }, 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def task_mark_incomplete(task_id):
    task = validate_task(task_id)

    request_body = request.get_json() 

    task.completed_at = None

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        }
    }, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details":f'Task {task.task_id} "{task.title}" successfully deleted'}), 200
    