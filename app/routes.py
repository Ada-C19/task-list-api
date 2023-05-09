from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app.models.goal import Goal
from app import db
# import pdb
import datetime
import os
from slack_sdk import WebClient

#All routes defined with tasks_bp start with url_prefix (/tasks)
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def get_valid_task_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({'details': f"Invalid data"}, 400))
    
    item = model.query.get(id)
    
    return item if item else abort(make_response({'details': f"Invalid data"}, 404))


@tasks_bp.route("", methods=['POST'])
def create_task():
    #Get the data from the request body
    request_body = request.get_json()

    if "description" not in request_body or "title" not in request_body:
        return{"details": "Invalid data"}, 400
    #Use it to make a Task
    new_task = Task.from_dict(request_body)
    new_task.completed_at = None
    #Persist (save, commit) it in the database
    db.session.add(new_task)
    db.session.commit()
    
    #Give back our response
    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("", methods=['GET'])
def get_tasks():
    task_query = request.args.get('sort')
    tasks_response = []
    #get tasks by query parameter

    if task_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif task_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    
    #get all tasks
    else:
        tasks = Task.query.all()
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_one_task(task_id):
    
    task = get_valid_task_by_id(Task, task_id)

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    task_to_update = get_valid_task_by_id(Task,task_id)
    
    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]
    
    db.session.commit()
    
    return {"task": task_to_update.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = get_valid_task_by_id(Task,task_id)
    
    if task_to_delete is None:
        return {"error": f"Task with ID {task_id} not found"}, 404
    
    db.session.delete(task_to_delete)
    db.session.commit()

    task_deleted_details = f"Task {task_id} \"{task_to_delete.title}\" successfully deleted" 
    return {"details": task_deleted_details }, 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def completed_task(task_id):
    updated_task=get_valid_task_by_id(Task, task_id)
    
    updated_task.completed_at = datetime.datetime.utcnow()
    db.session.commit()
    
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    client = WebClient(token=slack_token)
    
    result = client.chat_postMessage(
        channel="task-notifications",
        text=f"Someone just completed the task {updated_task.title}"
    )
    
    task_response = updated_task.to_dict()
    
    return make_response(({"task":task_response}), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    updated_task=get_valid_task_by_id(Task, task_id)
    
    updated_task.completed_at = None
    db.session.commit()
    
    task_response = updated_task.to_dict()
    
    return make_response(({"task":task_response}), 200)


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=['POST'])
def create_goal():
    #Get the data from the request body
    request_body = request.get_json()

    if "title" not in request_body:
        return{"details": "Invalid data"}, 400
    
    #Use it to make a new Goal
    new_goal = Goal.from_dict(request_body)
    #Persist (save, commit) it in the database
    db.session.add(new_goal)
    db.session.commit()
    
    #Give back our response
    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route("", methods=['GET'])
def get_goals():
    goals_query = request.args.get('sort')
    goals_response = []
    #get goals by query parameter

    if goals_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif goals_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    
    #get all goals
    else:
        goals = Goal.query.all()
    
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_one_goal(goal_id):
    
    goal = get_valid_task_by_id(Goal, goal_id)

    return {"goal": goal.to_dict()}, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal_to_delete = get_valid_task_by_id(Goal,goal_id)
    
    if goal_to_delete is None:
        return {"error": f"Goal with ID {goal_id} not found"}, 404
    
    db.session.delete(goal_to_delete)
    db.session.commit()

    goal_deleted_details = f"Goal {goal_id} \"{goal_to_delete.title}\" successfully deleted" 
    return {"details": goal_deleted_details }, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    request_body = request.get_json()
    goal_to_update = get_valid_task_by_id(Task,goal_id)
    
    goal_to_update.title = request_body["title"]
    
    db.session.commit()
    
    return {"goal": goal_to_update.to_dict()}, 200