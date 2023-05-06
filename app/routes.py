from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__,url_prefix="/tasks")

# helper function
def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"Task {id} is invalid"}, 400))
        
    task = Task.query.get(id)
    if not task:
        abort(make_response({"message":f"Task {id} not found" }, 404))
    return task
@task_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title = request_body["title"], description = request_body["description"])
        db.session.add(new_task)
        db.session.commit()
        response_dict = {}
        response_dict["task"]=new_task.to_dict()
        return make_response(response_dict, 201)
    except KeyError:
        details = {"details": "Invalid data"}

        return make_response(details, 400)

        
    
    return response_dict
@task_bp.route('', methods=['GET'])
def get_all_tasks():
    task_response = []
    tasks = Task.query.all()
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response)
    
@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)
    response_dict = {}
    response_dict["task"]=task.to_dict()
    return response_dict
    
@task_bp.route('/<task_id>', methods = ['PUT'])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body['title']
    task.description = request_body['description']
    
    db.session.commit()
    response_dict = {}
    response_dict["task"] = task.to_dict()
    return response_dict