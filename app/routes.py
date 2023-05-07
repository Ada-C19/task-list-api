from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
import pdb

#All routes defined with tasks_bp start with url_prefix (/tasks)
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def get_valid_task_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({'details': f"Invalid data"}, 400))
    
    item = model.query.get(id)
    
    return item if item else abort(make_response({'details': f"Invalid data"}, 404))


@tasks_bp.route("", methods=['POST'])
def create_task():
    #Get the data from the request body
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        return{"details": "Invalid data"}, 400
    #Use it to make a Task
    new_task = Task.from_dict(request_body)
    new_task.completed_at = None
    #Persist (save, commit) it in the database
    db.session.add(new_task)
    db.session.commit()
    
    #Give back our response
    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("", methods=['GET'])
def get_tasks():
    task_query = request.args.get('sort')
    
    #get tasks by query parameter

    if task_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif task_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    
    #get all tasks
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_one_task(task_id):
    
    task = get_valid_task_by_id(Task, task_id)

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    task_to_update = get_valid_task_by_id(Task,task_id)
    
    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]
    
    db.session.commit()
    
    return {"task": task_to_update.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = get_valid_task_by_id(Task,task_id)
    
    if task_to_delete is None:
        return {"error": f"Task with ID {task_id} not found"}, 404
    
    db.session.delete(task_to_delete)
    db.session.commit()

    task_deleted_details = f"Task {task_id} \"{task_to_delete.title}\" successfully deleted" 
    return {"details": task_deleted_details }, 200