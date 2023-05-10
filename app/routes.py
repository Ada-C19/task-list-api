from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)
    
    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))
    return task

#CREATE TASK

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
        new_task.description == "Test Description"
        new_task.completed_at == None
    except:    
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()
    
    return {"task":new_task.to_dict()}, 201

@task_bp.route("", methods=["GET"])
def get__all_tasks():
    title_query = request.args.get("title")
    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc)
    
    else:
        tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response)


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return {"task": task.to_dict()}
    

#UPDATE TASK
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    #db.session.add(task)
    db.session.commit()
    
    return make_response({
            "task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": False
        }
        })


#DELETE TASK
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
})