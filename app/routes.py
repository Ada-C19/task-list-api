from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

#CREATE
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    #create a new instance of Task
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body.get("completed_at", None)
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":{
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
        
    }}), 201


#GET ALL TASKS

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []   
    #to extract data from the database not from the task obj - REMINDER
    tasks = Task.query.all()

    for each_task in tasks:
        response.append({
            "id": each_task.task_id,
            "title": each_task.title,
            "description": each_task.description,
            "is_complete": False
        })

    return jsonify(response), 200

# #GET ONE
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
   

#check if task exists
    tasks = validate_task(task_id)

    return jsonify({"task": {
        "id": tasks.task_id,
        "title": tasks.title,
        "description": tasks.description,
        "is_complete": False

    }}), 200

#Update
@task_bp.route("/<id>", methods=["PUT"])
def update_planet(id):

    task = validate_task(id)
    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]
    task.completed_at = request_data.get("completed_at", None)

    db.session.commit()

    return jsonify({"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False

    }}), 200


#helper function

def validate_task(task_id):
    try:
        task_id_number = int(task_id)
    
    except ValueError:
        return abort(make_response({
            "error": f"invalid id {id} not found"}, 400
        ))
    
    task = Task.query.get(task_id_number)
    if task is None:
        abort(make_response({
            "error": "task not found"}, 404
        ))
    return task
