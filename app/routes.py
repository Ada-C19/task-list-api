from flask import Blueprint, jsonify, make_response, request
import os, requests
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.helper import validate_id, validate_goal

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


#get all tasks-"/tasks"-GET(read)
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200


#get one tasks-"/tasks/1"-GET(read)
@tasks_bp.route("/<id>", methods=["GET"])
def get_task(id):
    task = validate_id(id)
    return jsonify({"task":task.to_dict()}), 200


#create task-"/tasks"-POST(create)
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}), 400
    
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task":new_task.to_dict()}), 201


#update task-"tasks/1"-PUT(update)
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_id(id)
    request_body = request.get_json()
    task.update(request_body)
    db.session.commit()
    return jsonify({"task":task.to_dict()}), 200


#delete task-"tasks/1"-DELETE(delete)
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_id(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"details": f'Task {id} "{task.to_dict()["title"]}" successfully deleted'}), 200



#patch task-"tasks/1/mark_complete"-PATCH(update)
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    task = validate_id(id)
    request_body = request.get_json()
    task.patch_complete()
    db.session.commit()    

    SLACK_API_URL = "https://slack.com/api/chat.postMessage"
    if "SLACKBOT_TOKEN" is None:
        return jsonify({'error': 'Slackbot token not set'}), 500
    headers = {"Authorization": os.environ.get("SLACKBOT_TOKEN")}
    params = {
    'channel': 'task-notification',
    'text': f"Someone just completed the task {task.title}",
    }
    response = requests.post(SLACK_API_URL, headers=headers, json=params)
    if not response.ok:
        return jsonify({'error': 'Failed to send Slack message'}), 500

    return jsonify({"task":task.to_dict()}), 200


#patch task-"tasks/1/mark_incomplete"-PATCH(update)
@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    task = validate_id(id)
    request_body = request.get_json()
    task.patch_incomplete()
    db.session.commit()
    return jsonify({"task":task.to_dict()}), 200




#==========================WAVE5==========================




#get all goals-"/tasks"-GET(read)
@goals_bp.route("", methods=["GET"])
def get_all_goals():
    # if request.args.get("sort") == "asc":
    #     goals = Goal.query.order_by(Goal.title.asc())
    # elif request.args.get("sort") == "desc":
    #     goals = Goal.query.order_by(Goal.title.desc())
    # else:
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response), 200


#get one goals-"/goals/1"-GET(read)
@goals_bp.route("/<id>", methods=["GET"])
def get_goal(id):
    goal = validate_goal(id)
    return jsonify({"goal":goal.to_dict()}), 200


#create goal-"/goals"-POST(create)
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}), 400
    
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal":new_goal.to_dict()}), 201


#update goal-"goals/1"-PUT(update)
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()
    goal.update(request_body)
    db.session.commit()
    return jsonify({"goal":goal.to_dict()}), 200


#delete goal-"goals/1"-DELETE(delete)
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({"details": f'Goal {id} "{goal.to_dict()["title"]}" successfully deleted'}), 200


#patch goal-"goals/1/mark_complete"-PATCH(update)
@goals_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    goal = validate_id(id)
    request_body = request.get_json()
    goal.patch_complete()
    db.session.commit()    

    # SLACK_API_URL = "https://slack.com/api/chat.postMessage"
    # if "SLACKBOT_TOKEN" is None:
    #     return jsonify({'error': 'Slackbot token not set'}), 500
    # headers = {"Authorization": os.environ.get("SLACKBOT_TOKEN")}
    # params = {
    # 'channel': 'task-notification',
    # 'text': f"Someone just completed the task {task.title}",
    # }
    # response = requests.post(SLACK_API_URL, headers=headers, json=params)
    # if not response.ok:
    #     return jsonify({'error': 'Failed to send Slack message'}), 500

    return jsonify({"goal":goal.to_dict()}), 200


#patch goal-"goals/1/mark_incomplete"-PATCH(update)
@goals_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    goal = validate_id(id)
    request_body = request.get_json()
    goal.patch_incomplete()
    db.session.commit()
    return jsonify({"goal":goal.to_dict()}), 200