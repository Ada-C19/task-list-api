from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def make_a_task():
    try:
        request_body = request.get_json()

        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        return {
        "task": new_task.to_dict()}, 201
    except KeyError as error:
        return {"details": "Invalid data"}, 400

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        return sort_in_ascending_order()
    elif sort_query == "desc":
        return sort_in_descending_order()

    tasks = Task.query.all()
    
    task_response = []

    for task in tasks:
        task_response.append(task.to_dict())

    return jsonify(task_response)

def validate_model(model_class, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type ({type(model_id)}. Must be an integer)"}, 400))


    model = model_class.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{model_class.__name__} {model_id} does not exist."}, 404))
    
    return model

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    return {"task" :task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task,task_id)

    request_body = request.get_json()
    
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except:
        return {"details": "Invalid data"}, 404

    db.session.commit()
    return  {
        "task": task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task,task_id)
    db.session.delete(task)
    db.session.commit()
    return  {
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }, 200

def sort_in_ascending_order():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append(task)
    
    task_list = sorted(task_list, key = lambda task: task.title)
    task_list_dict = []
    for task in task_list:
        task_list_dict.append(task.to_dict())
    return jsonify(task_list_dict)

def sort_in_descending_order():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append(task)
    
    task_list = sorted(task_list, key = lambda task: task.title, reverse=True)
    task_list_dict = []
    for task in task_list:
        task_list_dict.append(task.to_dict())
    return jsonify(task_list_dict)