from flask import Blueprint,jsonify, request, make_response, abort
from app.models.task import Task
from app import db
import datetime


task_bp = Blueprint("tasks", __name__,url_prefix="/tasks")

#post a task
@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_task = Task.from_dict(request_body)
    


    db.session.add(new_task)
    db.session.commit()

    return {"task" : new_task.to_dict()}, 201


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        all_tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        all_tasks = Task.query.order_by(Task.title.desc())
    else:
        all_tasks = Task.query.all()

    for task in all_tasks:
        response.append(task.to_dict())

    return jsonify(response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_id(Task,task_id)

    return {"task" : task.to_dict()}, 200



@task_bp.route("<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)

    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()

    return {"task" : task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_not_complete(task_id):
    task = validate_id(Task, task_id)

    task.completed_at = None
    
    db.session.commit()
    return {"task" : task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task__is_complete(task_id):
    task = validate_id(Task, task_id)
    # request_data = request.get_json()

    task.completed_at = datetime.datetime.now()
    
    db.session.commit()
    return {"task" : task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}




def validate_id(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"msg": "invalid endpoint"},400))
    
    task = model.query.get(item_id)
    if not task:
        return abort(make_response({"msg": "invalid endpoint"},404))
    
    return task

