from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/task")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(new_task.to_dict(), 201)

@task_bp.route("", methods=["GET"])
def get_tasks():
    response_list = []

    all_tasks = Task.query.all()

    for task in all_tasks:
        response_list.append(task.to_dict())

    return jsonify(response_list), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = verify_item(Task, task_id)

    return make_response(task.to_dict() , 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = verify_item(Task, task_id)

    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()

    return make_response(task.to_dict() , 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = verify_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.task_id} \" {task.description} \" successfully deleted"})

def verify_item(model, item_id):
    try: 
        item_id = int(item_id)
    except ValueError:
        abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    return model.query.get_or_404(item_id)