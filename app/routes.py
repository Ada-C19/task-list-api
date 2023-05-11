from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# VALIDATE MODEL
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


# CREATE TASK
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)

    # if not (new_task.title and new_task.description):
    except KeyError as err:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    task_message = {}
    task_message["task"] = new_task.to_dict()

    return jsonify(task_message), 201


# GET SAVED TASKS
# @tasks_bp.route("", methods=["GET"])
# def get_saved_tasks():
#     tasks = Task.query.all()
#     tasks_list_response = []

#     for task in tasks:
#         tasks_list_response.append(task.to_dict())

#     return jsonify(tasks_list_response)


# GET ONE TASK
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    task_message = {"task": task.to_dict()}

    return jsonify(task_message)


# UPDATE TASK
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    task_message = {"task": task.to_dict()}

    return jsonify(task_message)


# DELETE TASK
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    task_message = {"details": f'Task {task.task_id} \"{task.title}\" successfully deleted'}

    return jsonify(task_message)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ WAVE 02 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Can this just replace GET SAVED TASKS???

# SORT TASKS BY TITLE  
@tasks_bp.route("", methods=["GET"])
def sort_by_title():
    # task_query = Task.query
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    task_response = [task.to_dict() for task in tasks]
    
    return jsonify(task_response)
