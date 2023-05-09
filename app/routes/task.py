from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    if not "title" in request_body or not "description" in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_task  = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)




@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    title_query = request.args.get("title")
    if title_query is None:
        all_tasks = Task.query.all()
    else:
        all_tasks = Task.query.filter_by(title = title_query)
    for task in all_tasks:
        response.append(task.to_dict())   
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_item(Task, task_id)
    return make_response({"task": task.to_dict()}, 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task, task_id)
    
    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_item(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200)

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id, description=f"{model.__name__} with id {item_id} not found")

