from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db



tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(cls, task_id):
    #handle invalid task id, return 400
    try:
        task_id = int(task_id)
    except: 
        abort(make_response({"msg": f"{cls.__name__} {task_id} is invalid."}, 400))
    
    task = Task.query.get(task_id)
    if task is None:
        abort(make_response({"msg": "Task not found."}, 404))

    return task 

 
    
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    title_query = request.args.get("title")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    #grab all info from the instance task table
    else:
        tasks = Task.query.all()
        
    task_dict = [task.to_dict() for task in tasks]
    return jsonify(task_dict), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def single_task(task_id):
    task = validate_task(Task,task_id)
    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    
    return jsonify({"task":task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_single_task(task_id):
    task = validate_task(Task, task_id)

    db.session.delete(task)    
    db.session.commit()

    success_message = f"Task {task.task_id} \"{task.title}\" successfully deleted"
    return jsonify({"details": success_message}), 200


@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")

    if not description or not title:
        return {"details": "Invalid data"}, 400

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at is not None}
    }, 201
