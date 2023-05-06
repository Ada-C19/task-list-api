from flask import Blueprint,request,make_response, jsonify, abort
from app import db
from app.models.task import Task 
from sqlalchemy import desc, asc 
from datetime import date 

tasks_bp = Blueprint("tasks",__name__,url_prefix="/tasks")

@tasks_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"]
                        )
    except:
        abort(make_response({
            "details":"Invalid data"
        },400))
    
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
    order_query = request.args.get("sort")
    
    if order_query == "desc":
        tasks = Task.query.order_by(desc("title"))
    else:
        tasks = Task.query.order_by(asc("title"))
        
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
    task = validate_task(task_id)
    
    return {
        "task":{
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete": False 
        }
    }
    
@tasks_bp.route("/<task_id>",methods=["PUT"])
def update_a_task(task_id):
    task = validate_task(task_id)
    
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
    task = validate_task(task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return {
        "details":f'Task {task.task_id} "{task.title}" successfully deleted'
    }

def validate_task(task_id):
    try: 
        task_id = int(task_id)
    except:
        abort(make_response({
            "message":f"Task {task_id} invalid"
        },400))
        
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({
            "message":f"Task {task_id} not found"
        },404))
    return task 

@tasks_bp.route("/<task_id>/mark_complete",methods=["PATCH"])
def mark_complete_on_incompleted(task_id):
    task = validate_task(task_id)
    
    task.completed_at = date.today() 
    
    db.session.commit()
    
    return {
        "task":{
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete": True 
        }
    }

@tasks_bp.route("/<task_id>/mark_incomplete",methods=["PATCH"])
def mark_incomplete_on_completed(task_id):
    task = validate_task(task_id)
    
    task.completed_at = None 
    
    db.session.commit()
    
    return {
        "task":{
            "id":task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete": False 
        }
    } 