from os import abort
import os
import requests
from app import db
from app.models.goal import Goal 
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


'''
Task CRUD Routes
'''
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if ("title" not in request_body) or ("description" not in request_body):
        return make_response({"details": "Invalid data"}, 400)
    
    new_task = Task.from_dict(request_body)
        
    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.response_dict()}, 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("sort")
    print("reading all tasks")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = [task.response_dict() for task in tasks]

    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_model(Task, task_id)
    return make_response({"task": task.response_dict()}, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    if task is None:
        return make_response({'message': f'Task {task.id} not found'}, 404)

    form_data = request.get_json()
    task.title = form_data["title"]
    task.description = form_data["description"]

    db.session.commit()
    return make_response({"task": task.response_dict()}, 200)

'''
Slack API - Message
'''
def slack_message_complete(message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"
    }
    params = {'channel': "task-notifications",
              'text': message}

    print("sending message")
    message = requests.post(url, data=params, headers=headers)
    return message.json()

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    
    if request.method == "PATCH":
        task = Task.query.get(task_id)

        if task is None:
            return make_response({"message":f"Task {task_id} not found"}, 404)
        
        task.completed_at = datetime.today()
        slack_message_complete(f"Congratulations! You've just completed the task '{task.title}'!")

        db.session.commit()

        return make_response({"task": task.response_dict()}, 200)
    
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if request.method == "PATCH":
        task = Task.query.get(task_id)

        if task is None:
            return make_response({"message":f"Task {task_id} not found"}, 404)
        
        task.completed_at = None

        db.session.commit()
        return make_response({"task": task.response_dict()}, 200)
    

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response({"message":f"Task {task_id} not found"}, 404)
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({'details' : f'Task {task.id} "{task.title}" successfully deleted'})

'''
Goal CRUD Routes
'''
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    else:
        new_goal = Goal(title = request_body["title"])
                    
    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": {"id": new_goal.id, "title": new_goal.title,}}, 201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.id,
            "title": goal.title})
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):    
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({"message" :f"Goal {goal_id} not found"}, 404)
    return make_response({"goal": {"id": goal.id, "title": goal.title}}, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({'message': f'Goal {goal_id} not found'}, 404)

    form_data = request.get_json()
    goal.title = form_data["title"]

    db.session.commit()
    return make_response({"goal": {"id": goal.id, "title": goal.title}}, 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({'message': f'Goal {goal_id} not found'}, 404)
    
    db.session.delete(goal)
    db.session.commit()

    return make_response({'details' : f'Goal {goal_id} "{goal.title}" successfully deleted'})

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal is None:
        return make_response({'message': f'Goal {goal_id} not found'}, 404)
    tasks = Task.query.join(Goal).filter(Task.goal_id == goal_id).all()
    task_list = []
    if tasks:
        for task in tasks:
            task_list.append(task.response_dict())

    if request.method == "GET":
        return make_response({
                "id": goal.id,
                "title": goal.title,
                "tasks": task_list 
        }, 200)
    
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_for_goal(goal_id):
        goal = Goal.query.get(goal_id)
    
        if goal is None:
            return make_response({'message': f'Goal {goal_id} not found'}, 404)
        tasks = Task.query.join(Goal).filter(Task.goal_id == goal_id).all()
        task_list = []
        if tasks:
            for task in tasks:
                task_list.append(task.response_dict())

        form_data = request.get_json()
        goal.tasks = []

        task_ids = form_data["task_ids"]
        for task_id in task_ids:
            task = Task.query.get(task_id)
            goal.tasks.append(task)

        db.session.commit()

        return make_response({
            "id": goal.id, 
            "task_ids": task_ids
        }, 200)