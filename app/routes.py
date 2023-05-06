from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task
from datetime import datetime

task_bp = Blueprint("task", __name__, url_prefix="/tasks")


#WAVE 1

#CREATE
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    #using class method - from_dict() from Task model
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return jsonify(
        {"task":new_task.task_to_dict()
        
    }), 201



# #GET ONE
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

#check if task_id exists
    task = validate_task(Task, task_id)

    return jsonify({"task": task.task_to_dict()}), 200

#Update
@task_bp.route("/<id>", methods=["PUT"])
def update_task(id):

    task = validate_task(Task, id)
    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]
    task.completed_at = request_data.get("completed_at", None)

    db.session.commit()

    return jsonify({"task": task.task_to_dict()}), 200

#Delete
@task_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):

    task = validate_task(Task, id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {id} "Go on my daily walk 🏞" successfully deleted'}, 200


#helper function

def validate_task(model, task_id):
    try:
        task_id = int(task_id)
    
    except ValueError:
        return abort(make_response({
            "error": f"invalid id {task_id} not found"}, 400
        ))
    
    task = model.query.get(task_id)
    if task is None:
        abort(make_response({
            "error": "task not found"}, 404
        ))
    return task

# #WAVE 2


@task_bp.route("", methods=["GET"])
def get_all_and_sort_title():

    response = []

    query = request.args.get("sort")

#check whether asc or desc
    if query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        #otherwise, get all
        tasks = Task.query.all()

    for each_task in tasks:
        response.append(each_task.task_to_dict())

    return jsonify(response), 200


#Mark InComplete
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(task_id):
    task = validate_task(Task, task_id)

    task = Task.query.get(task_id)
    
    #sets the task to incomplete regardless if it's complete or incomplete
    task.completed_at = None
    db.session.commit()
    

    return jsonify(
        {"task": task.task_to_dict()}
    ), 200

#Mark Complete
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task(task_id):
    task = validate_task(Task, task_id)

    task = Task.query.get(task_id)

#sets the current date 
    task.completed_at = datetime.now()
    db.session.commit()

    return jsonify({
        "task": task.task_to_dict()
    })





