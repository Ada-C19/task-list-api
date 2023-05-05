from flask import Blueprint,request,make_response, jsonify
from app import db
from app.models.task import Task 

tasks_bp = Blueprint("tasks",__name__,url_prefix="/tasks")

@tasks_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"]
                    )
    
    db.session.add(new_task)
    db.session.commit() 
    
    response_body = {
        "task":{
        "id":new_task.task_id,
        "title":new_task.title,
        "description":new_task.description,
        "is_complete":False 
        }
    }
    
    return make_response(response_body, 201)

@tasks_bp.route("",methods=["GET"])
def check_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete":False 
        })
    return jsonify(tasks_response) 

@tasks_bp.route("/<task_id>",methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get(task_id)
    return {
        "id":task.task_id,
        "title":task.title,
        "description":task.description,
        "is_complete":False 
    }
    
@tasks_bp.route("/<task_id>",methods=["PUT"])
def update_a_task(task_id):
    task = Task.query.get(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    
    return {
        "task":{
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete": False 
        }
    }
    
@tasks_bp.route("/<task_id>",methods=["DELETE"])
def delete_a_task(task_id):
    
    