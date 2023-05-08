from app import db 
from app.models.task import Task 
from flask import Blueprint, make_response,request, jsonify, abort

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task(): 
    request_body = request.get_json()


    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    )

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@task_bp.route("", methods=["GET"])
def get_all_tasks(): 
    response = []

    all_tasks = Task.query.all()

    for task in all_tasks: 
        response.append(task.to_dict())
    
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id): 
    task = validate_item(Task, task_id)
    return {"task": task.to_dict()}, 200 

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id): 
    task = validate_item(Task, task_id)

    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()

    return {"task": task.to_dict()} 

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id): 
    task = validate_item(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}

def validate_item(model, item_id):
    try: 
        item_id = int(item_id)
    except ValueError: 
        return abort(make_response({"msg": f"invalid id: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id)