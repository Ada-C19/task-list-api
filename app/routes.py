from flask import Blueprint, request, jsonify, abort, make_response
from app.models.task import Task
from app import db

def handle_valid_id(model, task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({'Error':f'Invalid id "{task_id}"'}, 400))

    task = model.query.get(task_id)

    return task if task else abort(make_response(
        {'Error':f'No {model.__name__} with id {task_id}'}, 404
        ))    

#Blueprint for tasks, all routes have url prefix (/tasks)
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if 'title' not in request_body or 'description' not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {
        "task":{
            "id":new_task.task_id,
            "title":new_task.title,
            "description":new_task.description,
            "is_complete": False
        }
    }, 201

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    #Retrieve a list of all the task objects in database
    all_tasks = Task.query.all()
    
    tasks_response = []
    for task in all_tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200

@tasks_bp.route("<task_id>", methods=["GET"])
def get_task(task_id):
    task = handle_valid_id(Task, task_id)

    return {"task": task.to_dict()}, 200

@tasks_bp.route("<task_id>", methods=["PUT"])
def update_task(task_id):
    request_body = request.get_json()
    
    #optionally, to only accept a put request if all attributes in task are being updated
    # if 'title' and 'description' not in request_body:
    #     return {'Error': ""}
    
    task_to_update = handle_valid_id(Task, task_id)
    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return {"task": task_to_update.to_dict()}, 200

@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_to_delete = handle_valid_id(Task, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{task_to_delete.title}" successfully deleted'
    }, 200
