from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
task_list_bp = Blueprint("task_list", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_list", __name__, url_prefix="/goals")
#validating the task_id
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"details": "Invalid Data"}, 404))
    return task

#validate goal_id
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"details": "Invalid Data"}, 404))
    return goal
    
# create tasks
@task_list_bp.route("", methods=["POST"])
def post_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        # completed_at = request_body["completed_at"]
    )
    db.session.add(new_task)
    db.session.commit() 
    return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "is_complete": False,
            "description": new_task.description
        }
    }), 201

#create goals 
@goals_bp.route("", methods=["POST"])
def post_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_goal = Goal(
        title = request_body["title"]
    )
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title} }), 201
# create nested post 
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    result = {"id": goal.goal_id,
  "task_ids": request_body["task_ids"]
}   
    for task_id in request_body["task_ids"]:
        task = validate_task(task_id)
        goal.tasks.append(task)
    db.session.commit()
    return result

# create nested get, singular goal, with its many tasks
@goals_bp.route("<goal_id>/tasks", methods=["GET"])
def get_tasks_one_goal(goal_id):
    goal = validate_goal(goal_id)
    task_response = []


    
    for task in goal.tasks:
        if not task.completed_at:
            task_response.append({
                "id": task.task_id,
                "goal_id":goal.goal_id,
                "title":task.title,
                "description": task.description,
                "is_complete": False

            })
        else:
            task_response.append({
                "id": task.task_id,
                "goal_id": goal.goal_id,
                "title": task.title,
                "description": task.description,
                "completed_at":task.completed_at
            })
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_response})
# #read all tasks
@task_list_bp.route("", methods=["GET"])
def get_all_tasks():
    task_response = []
    sort_query = request.args.get("sort")
    if sort_query == 'asc':
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    for task in tasks:
        if not task.completed_at:
            task_response.append({"id":task.task_id,
            "title":task.title,
            "description": task.description,
            "is_complete": False

            })
        else:
            task_response.append({
            "id":task.task_id,
            "title":task.title,
            "description": task.description,
            "completed_at":task.completed_at
        })
    return jsonify(task_response)

#read all goals
@goals_bp.route("", methods=["GET"]) 
def read_all_goals():
    goal_response = []
    goals = Goal.query.all()

    for goal in goals:
        if not goals:
            return jsonify(goal_response)
        else:
            goal_response.append({
            "id":goal.goal_id,
            "title":goal.title})

    return jsonify(goal_response)
#read one task/ read if empty task. 
@task_list_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    # goal = validate_goal(goal_id)
    
    if task.goal_id:
        return{"task": {
            "id":task.task_id,
            "goal_id": task.goal_id,
            "title":task.title,
            "description":task.description,
            "is_complete": True if task.completed_at else False}}
    else:
        return task.to_dict()
#read one goal 
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)


    return jsonify({"goal":{"id": goal.goal_id,
        "title":goal.title}})
# #update task
@task_list_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return task.to_dict()

#update goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit
    return goal.to_dict_goal()

#mark_complete endpoint with slack api implementation
@task_list_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_to_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    #slack implementation
    url = "https://slack.com/api/chat.postMessage"
    payload = json.dumps({
    "channel": "C0581AUJACV",
    "text": (f"Someone just completed the task {task.title}")
    })
    headers = {
    'Authorization': os.environ.get("SLACK_API_TOKEN"),
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    db.session.commit()
    return task.to_dict(), 200

#mark_incomplete endpoint
@task_list_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_to_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()
    return task.to_dict()

# delete task
@task_list_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return abort(make_response({"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}))

#delete goal:
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return abort(make_response({"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}))