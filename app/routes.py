from flask import Blueprint,jsonify, request, make_response, abort
from app.models.task import Task
from app import db


task_bp = Blueprint("tasks", __name__,url_prefix="/tasks")

#post a task
@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)
    
    # if "title" 

    db.session.add(new_task)
    db.session.commit()

    return {"task" : new_task.to_dict()}, 201


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    title_query = request.args.get("title")

    if title_query is None:
        all_tasks = Task.query.all()
    else:
        all_tasks = Task.query.filter_by(title=title_query)

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

