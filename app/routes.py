from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc, desc
from app import db
from app.say_bot import client
from app.models.task import Task
from datetime import datetime



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()
    try:
        new_task = Task.create_new_task(request_body)
        db.session.add(new_task)
        db.session.commit()

        message = Task.generate_message(new_task)

        return make_response(jsonify(message), 201)
    except KeyError as e:
        message = "Invalid data"
        return make_response({"details": message}, 400)

@tasks_bp.route("", methods = ["GET"])
def read_all_tasks():
    query_params = request.args.to_dict()
    tasks = filter_tasks_by_params(query_params)
    tasks_response = [task.task_to_dict() for task in tasks]
    return jsonify(tasks_response)

def filter_tasks_by_params(query_params):
    sort_by = query_params.get("sort")
    
    if sort_by:
        return get_sorted_tasks(query_params)
    
    if query_params:
        query_params = {k.lower(): v.title() for k, v in query_params.items()}
        tasks = Task.query.filter_by(**query_params).all()
    else:
        tasks = Task.query.all()
    
    return tasks

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    task = Task.query.get(task_id)
    task = Task.generate_message(task)
    return jsonify(task), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.update(request_body)

    db.session.commit()
    message = Task.generate_message(task)
    return make_response(jsonify(message))
          
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    message = {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
        }
    return make_response(jsonify(message), 200)

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        message = f"{cls.__name__} {id} is invalid"
        abort(make_response({"message": message}, 400))

    obj = cls.query.get(id)
    if not obj:
        abort(make_response(jsonify(message=f"{cls.__name__} not found"), 404))
    
    return obj

def get_sorted_tasks(query_params):
    sort_param = query_params.pop('sort', None)

    if sort_param == 'asc':
        return Task.query.filter_by(**query_params).order_by(Task.title.asc()).all()
    elif sort_param == 'desc':
        return Task.query.filter_by(**query_params).order_by(Task.title.desc()).all()
    else:
        return Task.query.filter_by(**query_params).order_by(Task.id.asc()).all()

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.is_complete = True
    task.completed_at = datetime.now()
    db.session.commit()

    client.chat_postMessage(
        channel="#task-notifications", 
        text=f"Someone just completed the task {task.title}"
    )
    
    message = Task.generate_message(task)
    return make_response(jsonify(message), 200)
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.is_complete = False
    task.completed_at = None
    db.session.commit()
    message = Task.generate_message(task)
    return make_response(jsonify(message), 200)