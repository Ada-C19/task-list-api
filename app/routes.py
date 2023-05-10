from flask import Blueprint,request,make_response, jsonify, abort
from app import db
from app.models.task import Task 
from app.models.goal import Goal 
from sqlalchemy import desc, asc 
from datetime import date 
import os
from dotenv import load_dotenv
import requests 
load_dotenv()

# CRUD for Tasks

tasks_bp = Blueprint("tasks",__name__,url_prefix="/tasks")

@tasks_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)

    except:
        abort(make_response({
            "details":"Invalid data"
        },400))
    
    db.session.add(new_task)
    db.session.commit() 
    
    response_body = {"task":new_task.to_dict()}
    
    return make_response(response_body, 201)

"""
Get all tasks - sort by descending order if users specify to do so, 
otherwise sort by ascending order by default
"""

@tasks_bp.route("",methods=["GET"])
def check_all_tasks():
    order_query = request.args.get("sort")
    
    if order_query == "desc":
        tasks = Task.query.order_by(desc("title"))
    else:
        tasks = Task.query.order_by(asc("title"))
        
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
        
    return jsonify(tasks_response) 

@tasks_bp.route("/<task_id>",methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return {"task":task.to_dict()}
    
@tasks_bp.route("/<task_id>",methods=["PUT"])
def update_a_task(task_id):
    task = validate_model(Task, task_id)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    
    return {"task":task.to_dict()}
    
@tasks_bp.route("/<task_id>",methods=["DELETE"])
def delete_a_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return {
        "details":f'Task {task.task_id} "{task.title}" successfully deleted'
    }

@tasks_bp.route("/<task_id>/mark_complete",methods=["PATCH"])
def mark_complete_on_incompleted(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = date.today() 
    
    db.session.commit()
    
    data = {
        "channel":"task-notifications",
        "text":f"Someone just completed the task {task.title}",
        "token":os.environ.get("BOT_API_KEY")
    }
    
    requests.post("https://slack.com/api/chat.postMessage",data)
    
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
    task = validate_model(Task, task_id)
    
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
    goal = validate_model(Goal, goal_id)
    
    return {
        "goal":{
            "id":goal.goal_id,
            "title":goal.title
        }
    }
    
@goals_bp.route("/<goal_id>",methods=["PUT"])
def update_a_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
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
    goal = validate_model(Goal,goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return {
        "details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }

# Build a helper function for id validation
def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({
            "message":f"{cls.__name__} {model_id} invalid"
        },400))
        
    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({
            "message":f"{cls.__name__} {model_id} not found"
        },404))
        
    return model

# Routes for one-to-many relationship

# Sending a list of task IDs to a goal
@goals_bp.route("/<goal_id>/tasks",methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    
    for id in task_ids:
        task = Task.query.get(id)
        goal.tasks.append(task) 
    
    db.session.commit() 
    
    response_body = {
        "id":goal.goal_id,
        "task_ids": task_ids
    }
    
    return make_response(response_body, 200)

# Getting tasks of one goal
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_to_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    
    return make_response(goal.to_dict(),200)
