
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
import datetime
import os

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({'msg': f"Invalid id '{id}'"}, 400))

    item = model.query.get(id)

    return item if item else abort(make_response({'msg': f'invalid data'}, 404))

# START OF TASK ROUTES

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
        new_task.completed_at = None
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@tasks_bp.route("", methods=['GET'])
def handle_tasks():
    task_query = request.args.get("sort")
    if task_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())

    elif task_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response), 200


@tasks_bp.route("<task_id>", methods=["GET"])
def handle_task(task_id):
    task = get_valid_item_by_id(Task, task_id)
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    request_body = request.get_json()
    task_to_update = get_valid_item_by_id(Task, task_id)

    # task_to_update.name = request_body["id"]
    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return {"task": task_to_update.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = get_valid_item_by_id(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task_to_delete.title}\" successfully deleted"}, 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = get_valid_item_by_id(Task, task_id)
    if task.completed_at is not None:
        return {"task": task.to_dict()}, 200
    task.completed_at = datetime.datetime.utcnow()
    db.session.commit()
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = get_valid_item_by_id(Task, task_id)
    if task.completed_at is None:
        return {"task": task.to_dict()}, 200
    task.completed_at = None
    db.session.commit()
    return {"task": task.to_dict()}, 200


# START OF GOAL ROUTES
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=['GET'])
def handle_goals():
    goal_query = request.args.get("sort")
    goals = Goal.query.all()

    goal_response = []
    for goal in goals:
        goal_response.append(goal.to_dict())
    return jsonify(goal_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_single_goal(goal_id):
    goal = get_valid_item_by_id(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
        new_goal.completed_at = None
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    request_body = request.get_json()
    goal_to_update = get_valid_item_by_id(Goal, goal_id)

    # task_to_update.name = request_body["id"]
    goal_to_update.title = request_body["title"]

    db.session.commit()

    return {"goal": goal_to_update.to_dict()}, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal_to_delete = get_valid_item_by_id(Goal, goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    return {"details": f"Goal {goal_id} \"{goal_to_delete.title}\" successfully deleted"}, 200

# NESTED ROUTES
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def handle_all_tasks_of_goals(goal_id):
        
    goal = get_valid_item_by_id(Goal, goal_id)
    goal_response = goal.to_dict_adding_task()
    return make_response(goal_response, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task_to_complete_goal(goal_id):
        
    goal = get_valid_item_by_id(Goal, goal_id)
    task_ids = request.json.get("task_ids", [])
    
    for task_id in task_ids:
        task = get_valid_item_by_id(Task, task_id)
        task.goal_id = goal_id

    db.session.commit()

    return make_response({"id": int(goal_id), "task_ids": task_ids}, 200)
