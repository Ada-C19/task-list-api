from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks_bp",__name__, url_prefix="/tasks")

@tasks_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()


    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": {"id":new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": (new_task.completed_at != None)}}, 201

@tasks_bp.route("",methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return {
        "task":{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": (task.completed_at != None)}}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_to_update = validate_task(task_id)

    request_body = request.get_json()

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task_to_update.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return abort(make_response({"details":f"Task {task_id} \"{task.title}\" successfully deleted"}, 404))