from app import db
from .models.task import Task
from sqlalchemy import asc, desc
from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if request_body.get("title") is None or request_body.get("description") is None:
        return make_response ({"details": "Invalid data"}, 400)
    
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response = {"task": new_task.to_dict()}

    return make_response(jsonify(response), 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    order_param = request.args.get("sort")

    
    if order_param == "asc" :
        tasks = Task.query.order_by(Task.title.asc())
    elif order_param == "desc": 
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    task_list=[task.to_dict()for task in tasks]

    return jsonify(task_list), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_planet(task_id):

    task = validate_model(Task, task_id)
    response = {"task": task.to_dict()}

    return make_response(jsonify(response), 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task=validate_model(Task, task_id)
    request_body=request.get_json()

    if request_body.get("title") is None or request_body.get("description") is None:
        return make_response(f"Some additional information needed to update task{task.task_id}{task.title}",400)

    task.title=request_body["title"]
    task.description=request_body["description"]
    

    db.session.commit()

    response = {"task": task.to_dict()}

    return make_response(jsonify(response), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()
    response = {"details": (f"Task {task.task_id} \"{task.title}\" successfully deleted")}

    return make_response(jsonify(response), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None 
    db.session.commit()
    
    response = {"task": task.to_dict()}

    return make_response(jsonify(response), 200)
    

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    response = {"task": task.to_dict()}

    return make_response(jsonify(response), 200)
      





# datetime.utcnow()

# HELPER FUNCTION
def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} was invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} with id {id} was not found"}, 404))
    
    return model