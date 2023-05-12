from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal

from flask import Blueprint, jsonify, abort, make_response, request
import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")


@task_bp.route("", methods=["POST"])
def make_a_task():
    try:
        request_body = request.get_json()

        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        return {
        "task": new_task.to_dict()}, 201
    except KeyError as error:
        return {"details": "Invalid data"}, 400

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        return sort_in_ascending_order()
    elif sort_query == "desc":
        return sort_in_descending_order()

    tasks = Task.query.all()
    
    task_response = []

    for task in tasks:
        task_response.append(task.to_dict())

    return jsonify(task_response)

def validate_model(model_class, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type ({type(model_id)}. Must be an integer)"}, 400))


    model = model_class.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{model_class.__name__} {model_id} does not exist."}, 404))
    
    return model

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    if not task.goal:
        return {"task" :task.to_dict()}, 200
    else:
        return {"task" :task.goal_to_dict()}, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task,task_id)

    request_body = request.get_json()
    
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except:
        return {"details": "Invalid data"}, 404

    db.session.commit()
    return  {
        "task": task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task,task_id)
    db.session.delete(task)
    db.session.commit()
    return  {
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }, 200

def sort_in_ascending_order():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append(task)
    
    task_list = sorted(task_list, key = lambda task: task.title)
    task_list_dict = []
    for task in task_list:
        task_list_dict.append(task.to_dict())
    return jsonify(task_list_dict)

def sort_in_descending_order():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append(task)
    
    task_list = sorted(task_list, key = lambda task: task.title, reverse=True)
    task_list_dict = []
    for task in task_list:
        task_list_dict.append(task.to_dict())
    return jsonify(task_list_dict)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_title_as_complete(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = datetime.datetime.now()
    
    db.session.commit()
    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_title_as_incomplete(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = None
    
    db.session.commit()
    return {"task": task.to_dict()}, 200

@goal_bp.route("", methods=["POST"])
def make_a_goal():
    try:
        request_body = request.get_json()

        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        return {
        "goal": new_goal.to_dict()}, 201
    except KeyError as error:
        return {"details": "Invalid data"}, 400

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    
    goal_response = []

    for goal in goals:
        goal_response.append(goal.to_dict())
    return jsonify(goal_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    return {"goal" : goal.to_dict()}, 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    request_body = request.get_json()
    
    try:
        goal.title = request_body["title"]
    except:
        return {"details": "Invalid data"}, 404

    db.session.commit()
    return  {
        "goal": goal.to_dict()}, 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    db.session.delete(goal)
    db.session.commit()

    return  {
        "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    }, 200

@goal_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_list_of_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    task_list = request_body.get("task_ids")
    for task_id in task_list:
        new_task = validate_model(Task, task_id)
        new_task.goal_id = goal.goal_id
        new_task.goal = goal
    db.session.commit()
    return {"id": goal.goal_id, "task_ids": task_list}, 200

@goal_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_list = []
    for task in goal.tasks:
        task_list.append(task.goal_to_dict())
    
    return {
        "id" : goal.goal_id,
        "title": goal.title, 
        "tasks": task_list
    }
