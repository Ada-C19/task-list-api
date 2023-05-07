from flask import Blueprint,request,make_response, jsonify, abort
from app import db
from app.models.task import Task 
from app.models.goal import Goal 
from sqlalchemy import desc, asc 
from datetime import date 

# CRUD for Tasks

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

# CRUD for Goals

goals_bp = Blueprint("goals",__name__,url_prefix="/goals")

@goals_bp.route("",methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        abort(make_response({
            "details":"Invalid data"
        },400))
    
    db.session.add(new_goal)
    db.session.commit() 
    
    response_body = {
        "goal":{
        "id":new_goal.goal_id,
        "title":new_goal.title,
        }
    }
    
    return make_response(response_body, 201)

@goals_bp.route("",methods=["GET"])
def check_all_goals():
    goals = Goal.query.all()
        
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id":goal.goal_id,
            "title":goal.title
        })
        
    return jsonify(goals_response) 

@goals_bp.route("/<goal_id>",methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    
    return {
        "goal":{
            "id":goal.goal_id,
            "title":goal.title
        }
    }
    
@goals_bp.route("/<goal_id>",methods=["PUT"])
def update_a_goal(goal_id):
    goal = validate_goal(goal_id)
    
    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()
    
    return {
        "goal":{
            "id":goal.goal_id,
            "title":goal.title
        }
    }
    
@goals_bp.route("/<goal_id>",methods=["DELETE"])
def delete_a_goal(goal_id):
    goal = validate_goal(goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return {
        "details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }

def validate_goal(goal_id):
    try: 
        goal_id = int(goal_id)
    except:
        abort(make_response({
            "message":f"Goal {goal_id} invalid"
        },400))
        
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({
            "message":f"Goal {goal_id} not found"
        },404))
    return goal