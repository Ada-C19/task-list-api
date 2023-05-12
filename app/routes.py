import os
from datetime import datetime
import requests
from app import db

from flask import Blueprint, jsonify, make_response, request, abort

from app.models.task import Task
from app.models.goal import Goal


# DEFINING THE BLUEPRINTS
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# error handling
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"task {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": f"{cls.__name__} id {model_id} not found"}, 404))

    return model


# ============================= CRUD ROUTES  =============================
# CREATE TASK- POST request to /tasks
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dic(), 201
    

# READ ALL TASKS- GET request to /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sorted_by_query = request.args.get("sort")
    title_query = request.args.get("title")
    
    if sorted_by_query== "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sorted_by_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif sorted_by_query == "id":
        tasks = Task.query.order_by(Task.task_id).all()
    elif title_query:
        tasks = Task.query.filter_by(title=title_query).all()
    
    if not sorted_by_query:  
        tasks= Task.query.all()
    
    task_response = [task.to_dic()["task"] for task in tasks]
    return jsonify(task_response), 200


# READ ONE TASK- GET request to /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dic(), 200


# UPDATE TASK- PUT request to /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    
    return task.to_dic(), 200
    
    
# mark complete on a complete task
# UPDATE TASK- PATCH request to /tasks/<task_id>/mark_complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task,task_id)
    
    task.completed_at=datetime.utcnow()
    
    db.session.commit()
    
    # ID of the channel you want to send the message to
    channel_id = "C057AARLUNR"
    
    slack_url = "https://slack.com/api/chat.postMessage"
    
    slack_data = {
        "channel": channel_id,
        "text": f"Someone completed the {task.title} task!"
    }
    
    headers= {
        "Authorization": f"Bearer {os.environ.get('SLACK_KEY')}"
    }
    
    slack_request = requests.post(slack_url, headers=headers, json=slack_data)
    print(slack_request.text)
    
    return task.to_dic(), 200


# mark incomplete on an complete task
# UPDATE TASK- PATCH request to /tasks/<task_id>/mark_incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task,task_id)

    task.completed_at= None
    
    db.session.commit()
    
    return task.to_dic(), 200


# DELETE TASK- DELETE request to /tasks/<task_id>
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_book(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return { "details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200



# CREATE GOAL- POST request to /goals
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title,
    }}, 201  



# READ ALL GOALS- GET request to /goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
        
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
        })
    return jsonify(goals_response), 200

# READ ONE GOAL- GET request to /goals/<goal_id>
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return { "goal": {
        "id": goal.goal_id,
        "title": goal.title,
        }
    }, 200
    
    
# UPDATE GOAL- PATCH request to /goals/<goal_id>/mark_incomplete
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    title = request_body["title"]

    db.session.commit()

    return goal.to_dic()

# DELETE GOAL- DELETE request to /goals/<goal_id>
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({'details': f'Goal {goal_id} \"{goal.title}\" successfully deleted'}, 200)

@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    for id in request_body["task_ids"]:
        task = validate_model(Task, id)
        goal.tasks.append(task)
    
    db.session.commit()
    
    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = goal.task_by_goal_id()
    
    return jsonify(tasks_response)
    
    

