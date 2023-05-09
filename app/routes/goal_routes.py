from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import requests, os

goal_list_bp = Blueprint("goal_list_bp", __name__, url_prefix="/goals")

# Create new goal
@goal_list_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()
    
    return {"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title
        } }, 201
    
# Get all saved goals or zero saved goals
@goal_list_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append( {
            "id": goal.goal_id,
            "title": goal.title
            } )
    return jsonify(goals_response)

# Get one goal
@goal_list_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    return {"goal": {
        "id": goal.goal_id,
        "title": goal.title
    } }
    
# Update goal
@goal_list_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    request_data = request.get_json()
    
    goal.title = request_data["title"]
    
    db.session.commit()
    
    return {"goal": {
        "id": goal.goal_id,
        "title": goal.title
    }}
    
# Delete goal
@goal_list_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}

# Add 3 tasks to 1 goal
@goal_list_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()
    # request_body is a dict
    
    task_ids_list = request_body["task_ids"]
    # pull out list of task IDs
    
    for task_id in task_ids_list:
        task = Task.query.get(task_id)
        if not task:
            new_task = Task(task_id=task_id, 
                            goal=goal)
            db.session.add(new_task)
        else:
            task.goal = goal
                        
        db.session.commit()
    
    return {"id": goal.goal_id,
            "task_ids": task_ids_list}

# Get tasks of 1 goal
@goal_list_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    # Ask how to jsonify this list w/o causing errors???
    tasks_response = []
    jsonify(tasks_response)
    
    for task in goal.tasks:
        tasks_response.append(
            {"id": task.task_id,
            "goal_id": goal.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete_status(task.completed_at)}
        )
    
    return {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
    }

# Getting Tasks of One Goal: No Matching Tasks
@goal_list_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_one_goal_no_tasks(goal_id):
    goal = validate_item(Goal, goal_id)
    
    if len(goal.tasks) == 0:
        return {
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": []
        }

# Getting Tasks of One Goal: No Matching Goal
@goal_list_bp.route("/<goal_id>/tasks",methods=["GET"])
def get_tasks_for_one_goal_no_goal(goal_id):
    validate_item(Goal, goal_id)

# No matching Goal: Get, Update, and Delete
# Helper function
def validate_item (model, item_id):
    try:
        item_id_int = int(item_id)
    except:
        return abort(make_response({"message":f"Item {item_id} invalid"}, 400))
    
    item = model.query.get(item_id_int)
    
    if not item:
        return abort(make_response({"message":f"Item {item_id_int} not found"}, 404))
    
    return item    
    
# Helper function
def is_complete_status(completed_at):
    if completed_at is None:
        return False
    else:
        return True