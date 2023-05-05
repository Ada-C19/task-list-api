from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task

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
    tasks = validate_task(Task, task_id)

    return jsonify({"task": {
        "id": tasks.task_id,
        "title": tasks.title,
        "description": tasks.description,
        "is_complete": False

    }}), 200

#Update
@task_bp.route("/<id>", methods=["PUT"])
def update_task(id):

    task = validate_task(Task, id)
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
# @task_bp.route("/tasks", methods=["GET"])
# def sort_title_asc():
    
#     response = []
    
#     #check for sort as param
#     task_sort = request.args.get("sort")

#     sort_query = request.args.get("sort")
#     task_title = Task.title

#     if sort_query == "asc":
#         tasks = Task.query.order_by(task_title)



