from flask import abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import timezone, datetime

def get_task_instance(request):
    task_info = validate_data(request)
    return Task.from_dict(task_info)

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Invalid task ID: {task_id}"}, 400))
    return task_id

def get_task_by_id(task_id):
    task_id = validate_task_id(task_id)
    task = db.session.get(Task, task_id)

    if not task:
        abort(make_response({'message': f'Task {task_id} was not found.'}, 404))
        
    return task 

def update_task_from_request(task, request):
    task_info = request.get_json()

    if 'title' in task_info:
        task.title = task_info['title']
    if 'description' in task_info:
        task.description = task_info['description']
    if 'completed_at' in task_info:
        task.completed_at = task_info['completed_at']
    else:
        task.completed_at = None

    return task

def validate_data(request):
    task_info = request.get_json()
    if not "title" in task_info or not "description" in task_info:
        abort(make_response({"details": "Invalid data"}, 400))
    if not "completed_at" in task_info:
        task_info["completed_at"] = None
    return task_info

def get_goal_instance(request):
    goal_info = validate_goal_data(request)
    return Goal.from_dict(goal_info)

def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Invalid goal ID: {goal_id}"}, 400))

    return goal_id

def get_goal_by_id(goal_id):
    goal_id = validate_goal_id(goal_id)
    goal = db.session.get(Goal, goal_id)

    if not goal:
        abort(make_response({'message': f'Goal {goal_id} was not found.'}, 404))
        
    return goal 

def update_goal_from_request(goal, request):
    goal_info = request.get_json()

    if 'title' in goal_info:
        goal.title = goal_info['title']

    return goal

def validate_goal_data(request):
    goal_info = request.get_json()
    if not "title" in goal_info:
        abort(make_response({"details": "Invalid data"}, 400))
    return goal_info
