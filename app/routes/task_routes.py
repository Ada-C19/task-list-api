from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    verify_task_inputs(request_body)
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_dict = message_for_only_one_task(new_task)

    return make_response(response_dict, 201)

@task_bp.route("", methods=["GET"])
def get_tasks():
    response_list = []
    sort_query = request.args.get("sort")

    all_tasks = Task.query.all()

    for task in all_tasks:
        response_list.append(task.to_dict())

    if sort_query == "asc":
        response_list.sort(key=get_title)
    elif sort_query == "desc":
        response_list.sort(reverse=True, key=get_title)

    return jsonify(response_list), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = verify_item(Task, task_id)

    response_dict = message_for_only_one_task(task)

    return make_response(response_dict, 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = verify_item(Task, task_id)

    request_body = request.get_json()
    verify_task_inputs(request_body)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_dict = message_for_only_one_task(task)
    return make_response(response_dict, 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = verify_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"})

def verify_item(model, item_id):
    try: 
        item_id = int(item_id)
    except ValueError:
        abort(make_response({"message": f"Invalid id: {item_id}"}, 400))
    item = model.query.get(item_id)
    if item:
        return item 
    else:
        abort(make_response({"message": f"Item ID not found: {item_id}"}, 404))

def verify_task_inputs(request_body):
    if "title" in request_body and "description" in request_body:
        return request_body
    abort(make_response({"details": "Invalid data"}, 400))

def message_for_only_one_task(task):
    return {"task": task.to_dict()}

def get_title(task):
    return task["title"]