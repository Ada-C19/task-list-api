from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os
import requests

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"details": f"{cls.__name__} {model_id} is not found"}, 404))
    
    return model

def validate_request(cls, request):
    request_body = request.get_json()

    if not request_body.get("title"):
        abort(make_response({"details":"Invalid data"}, 400))
    
    elif not request_body.get("description") and cls == Task:
        abort(make_response({"details":f"Invalid data"}, 400))
    
    return request_body
  

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = validate_request(Task, request)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.to_dict()}, 201

@task_bp.route("", methods=["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort", "asc")
    title_query = request.args.get("title")
    description_query = request.args.get("description")
   

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())

    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())

    elif title_query:
        tasks = Task.query.filter_by(title = title_query)

    elif description_query:
        tasks = Task.query.filter_by(description = description_query)

    else:
        tasks = Task.query.all()

    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200
   

@task_bp.route("/<id>", methods=["GET"])
def read_single_task(id):
    task = validate_model(Task, id)

    goal = Goal.query.get(id)

    if goal != None:
        task_dict = task.to_dict()
        task_dict["goal_id"] = goal.goal_id

    else:
        task_dict = task.to_dict()

    return ({"task":task_dict}),200
    

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title  = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return task.to_dict_one_task(), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details":f'Task {task_id} "{task.title}" successfully deleted'}), 200

    
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at is not None:
        task.completed_at = None
    
    task.is_complete = False
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("<task_id>/mark_complete", methods=['PATCH'])
def mark_task_complete_slack(task_id):
    task = validate_model(Task, task_id)
    
    if task.completed_at is not None:
        return jsonify({"task": task.to_dict()}), 200
    
    task.completed_at = datetime.utcnow()
    db.session.commit()

    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    SLACK_CHANNEL = '#task-notifications'

 #respone notification to Slack

    message = f"Someone just completed the task{task.title}"
    slack_data = {'text': message, 'channel': SLACK_CHANNEL}
    headers = {'Authorization': f'Bearer {SLACK_BOT_TOKEN}'}
    
    try:
        response = requests.post('https://slack.com/api/chat.postMessage', json=slack_data, headers=headers)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Failed to send Slack notification: {e}'})

    return jsonify({"task": task.to_dict()}), 200

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")
@goal_bp.route("", methods=['POST'])

# creating a goal resource
def create_goal():
    request_body = validate_request(Goal, request)

    new_goal = Goal(
        title=request_body["title"]
    )
    
    db.session.add(new_goal)
    db.session.commit()
    
    return ({"goal":new_goal.goal_dict()}), 201

@goal_bp.route("", methods=['GET'])
def read_all_goals():
    goals = Goal.query.all()
        
    goals_response = []
    
    for goal in goals:
        goals_response.append({ "title": goal.title, "id": goal.goal_id})
    
    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=['GET'])
def read_one_goal(goal_id):
    
    goal = validate_model(Goal, goal_id)
     
    return ({"goal": goal.goal_dict()}), 200

@goal_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title  = request_body["title"]
    db.session.commit()

    return jsonify({"goal": goal.goal_dict()}), 200

@goal_bp.route("/<goal_id>", methods=['DELETE'])
def delete_task(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details":f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])

def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    if 'task_ids' not in request.json:
        abort(400)

    task_ids = request.json['task_ids']

    tasks = Task.query.filter(Task.task_id.in_(task_ids)).all()

    if len(tasks) != len(task_ids):
        abort(400)

    goal.task_ids = task_ids

    for task in tasks:
        task.goal_id = goal_id

    db.session.commit()

    return jsonify({'id': goal.goal_id, 'task_ids': goal.task_ids})

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []

    for task in goal.tasks:
        task_dict = task.to_dict()
        task_dict["goal_id"] = goal.goal_id
        tasks_response.append(task_dict)

    goal_dict = goal.goal_dict()
    goal_dict["tasks"] = tasks_response

    return jsonify(goal_dict), 200








    
    
    
    







    






