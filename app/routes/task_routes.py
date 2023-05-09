from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from app.helpers import validate_model


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#ROUTE 1
@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        return make_response({"task":new_task.to_dict()}, 201)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

#ROUTE 2
@tasks_bp.route("", methods=["GET"])
def get_saved_tasks():
    sort_order = request.args.get("sort")

    if sort_order:
        if sort_order == "asc":
            tasks = Task.query.order_by(Task.title.asc())
    
        if sort_order == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response)



#ROUTE 3
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    try:
        task = validate_model(Task, task_id)

        return make_response({"task": task.to_dict()}, 200)
    except KeyError:
        abort(make_response({'details': f"Task {task_id} not found"}, 404))


#ROUTE 4
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    try:
        task_data = request.get_json()
        task_to_update = validate_model(Task, task_id)

        task_to_update.title = task_data["title"]
        task_to_update.description = task_data["description"]

        db.session.commit()

        return make_response({"task": task_to_update.to_dict()}, 200)
    except KeyError:
        abort(make_response({'details': f"Task {task_id} not found"}, 404))

#ROUTE 5
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    try:
        task = validate_model(Task, task_id)

        db.session.delete(task)
        db.session.commit()


        message = {"details": f'Task {task_id} "{task.title}" successfully deleted'}
        return make_response(message, 200)
    
    except KeyError:
        abort(make_response({'details': f"Task {task_id} not found"}, 404))