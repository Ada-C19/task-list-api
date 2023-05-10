from flask import Blueprint, request, make_response, jsonify, abort
from .models.task import Task
from .models.goal import Goal
from app import db
from datetime import datetime
import requests
import os

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

# Read all tasks:
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("sort") 

    if title_query == "asc":
        task_objects = Task.query.order_by(Task.title) 
        # task_objects = Task.query.order_by(Task.title).all()
    elif title_query == "desc":
        task_objects = Task.query.order_by(Task.title.desc()) 
    else:
        task_objects = Task.query.all()
    task_list = [Task.to_dict(task) for task in task_objects]
    return make_response(jsonify(task_list), 200)
 
 # Read one task:
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task_object_list = validate_model(Task, task_id)#Task.query.filter_by(task_id=task_id).all()
    # task_list = [Task.to_dict(task) for task in task_object]
    # return make_response(jsonify(task_list), 200)
    response = Task.add_task_key(Task.to_dict(task_object_list))
    return make_response(response, 200)

# Create task:
@task_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body_dict = request.get_json()
        task_object = Task.from_dict(request_body_dict)
        db.session.add(task_object)
        db.session.commit()
        response_object_list = Task.query.all()
        # response_body ={"task":{"id":response_object[0].task_id,
        #                         "title":request_body_dict["title"],
        #                         "description":request_body_dict["description"],
        #                         "is_complete": False}} #request_body["completed_at"]
        response_dict = Task.to_dict(response_object_list[0])
        return make_response(Task.add_task_key(response_dict), 201)
    except(KeyError):
        return make_response({"details": "Invalid data"}, 400)
    
# Replace a task
@task_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    task_object = validate_model(Task, task_id)
    task_request_body_dict = request.get_json()

    if task_request_body_dict.get("title"):
        task_object.title = task_request_body_dict.get("title")
    if task_request_body_dict.get("description"):
        task_object.description = task_request_body_dict.get("description")
    if task_request_body_dict.get("completed_at"):
        task_object.complete_at = task_request_body_dict.get("completed_at")
    db.session.commit()
    return Task.add_task_key(Task.to_dict(task_object))

# Delete a task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    response_object = validate_model(Task, task_id)
    db.session.delete(response_object)
    db.session.commit()
    return make_response({
        'details': f'Task {response_object.task_id} "{response_object.title}" successfully deleted'}, 200)

# Update a task, mark complete
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_mark_complete(task_id):
    task_object = validate_model(Task, task_id)
    task_object.completed_at = datetime.utcnow()
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    API_KEY = "Bearer xoxb-4680452269380-5222659283431-QKg66zTyHbkT2F9a9Dq51ebD"#os.environ.get(API_KEY)
    headers = {
        "Authorization" : API_KEY}
    
    data = {"channel": "api-test-channel",
    "text" :  f"Task #{task_id} is complete!"}

    response = requests.post(url, headers=headers, json=data)
    print(response)
    return Task.add_task_key(Task.to_dict(task_object))


# Update a task, mark incomplete
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_mark_incomplete(task_id):
    task_object = validate_model(Task, task_id)
    task_object.completed_at = None
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    API_KEY = "Bearer xoxb-4680452269380-5222659283431-QKg66zTyHbkT2F9a9Dq51ebD"#os.environ.get(API_KEY)
    headers = {
        "Authorization" : API_KEY}
    
    data = {"channel": "api-test-channel",
    "text" :  f"Task #{task_id} is incomplete!"}

    response = requests.post(url, headers=headers, json=data)
    print(response)
    return Task.add_task_key(Task.to_dict(task_object))


def validate_model(cls, task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details" : f"It is not a valid id {task_id}"}, 400))
    response = cls.query.get(task_id)
    if not response:
        abort(make_response({"details" : f"{cls.__name__} #{task_id} not found"}, 404))
    return response

#======================================
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")
# Read all goals:
@goal_bp.route("", methods=["GET"])
def get_all_goals():
    title_query = request.args.get("sort") 

    if title_query == "asc":
        goal_objects = Goal.query.order_by(Goal.title) 
        # goal_objects = goal.query.order_by(goal.title).all()
    elif title_query == "desc":
        goal_objects = Goal.query.order_by(Goal.title.desc()) 
    else:
        goal_objects = Goal.query.all()
    goal_list = [Goal.to_dict(goal) for goal in goal_objects]
    return make_response(jsonify(goal_list), 200)
 
 # Read one goal:
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal_object_list = validate_model(Goal, goal_id)#goal.query.filter_by(goal_id=goal_id).all()
    # goal_list = [goal.to_dict(goal) for goal in goal_object]
    # return make_response(jsonify(goal_list), 200)
    response = Goal.add_goal_key(Goal.to_dict(goal_object_list))
    return make_response(response, 200)

# Create goal:
@goal_bp.route("", methods=["POST"])
def create_a_goal():
    try:
        request_body_dict = request.get_json()
        goal_object = Goal.from_dict(request_body_dict)
        db.session.add(goal_object)
        db.session.commit()
        response_object_list = Goal.query.all()
        # response_body ={"goal":{"id":response_object[0].goal_id,
        #                         "title":request_body_dict["title"],
        #                         "description":request_body_dict["description"],
        #                         "is_complete": False}} #request_body["completed_at"]
        response_dict = Goal.to_dict(response_object_list[0])
        return make_response(Goal.add_goal_key(response_dict), 201)
    except(KeyError):
        return make_response({"details": "Invalid data"}, 400)
    
# Replace a goal
@goal_bp.route("/<goal_id>", methods=["PUT"])
def replace_a_goal(goal_id):
    goal_object = validate_model(Goal, goal_id)
    goal_request_body_dict = request.get_json()

    if goal_request_body_dict.get("title"):
        goal_object.title = goal_request_body_dict.get("title")
    if goal_request_body_dict.get("description"):
        goal_object.description = goal_request_body_dict.get("description")
    if goal_request_body_dict.get("completed_at"):
        goal_object.complete_at = goal_request_body_dict.get("completed_at")
    db.session.commit()
    return Goal.add_goal_key(Goal.to_dict(goal_object))

# Delete a goal
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_a_goal(goal_id):
    response_object = validate_model(Goal, goal_id)
    db.session.delete(response_object)
    db.session.commit()
    return make_response({
        'details': f'Goal {response_object.goal_id} "{response_object.title}" successfully deleted'}, 200)


