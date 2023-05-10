from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
import requests
from datetime import datetime
import os
from app.routes.task import validate_item

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")
@goal_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()
    if not "title" in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_goal  = Goal.from_dict(request_body)
    
    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)
@goal_bp.route("", methods=["GET"])
def get_goals():
    response = []
    title_query = request.args.get("title")
    if title_query is None:
        all_goals = Goal.query.all()
    else:
        all_goals = Goal.query.filter_by(title = title_query)
    for goal in all_goals:
        response.append(goal.to_dict())   
    return jsonify(response), 200
# @goal_bp.route("", methods=["GET"])
# def get_goals():
#     sort_direction = request.args.get("sort", default="desc")
#     if sort_direction == "asc":
#         all_goals = Goal.query.order_by(Goal.title.asc())
#     else:
#         all_goals = Goal.query.order_by(Goal.title.desc())
    
#     response = [goal.to_dict() for goal in all_goals]
#     return jsonify(response), 200


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    return make_response({"goal": goal.to_dict()}, 200)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    request_data = request.get_json()

    goal.title = request_data["title"]

    db.session.commit()

    return make_response({"goal": goal.to_dict()}, 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}, 200)

# def validate_item(model, item_id):
#     try:
#         item_id = int(item_id)
#     except ValueError:
#         return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
#     return model.query.get_or_404(item_id, description=f"{model.__name__} with id {item_id} not found")

@goal_bp.route("/<goal_id>/<complete_status>", methods=["PATCH"])
def mark_complete(goal_id, complete_status):
    goal = validate_item(Goal, goal_id)
    if complete_status == "mark_complete":
        goal.completed_at = datetime.now()
        # requests.post("https://slack.com/api/chat.postMessage", json={"channel": "task-notifications", "text": f"Someone just completed the task {task.title}"}, headers={"Authorization": os.environ.get("SLACK_BOT_TOKEN")})
    elif complete_status == "mark_incomplete":
        goal.completed_at = None
    db.session.commit()
    return make_response({"goal": goal.to_dict()}, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    request_body = request.get_json()

    task_ids = request_body["task_ids"]
    goal.tasks = [Task.query.get(id) for id in task_ids]

    db.session.commit()

    return jsonify(id=goal.goal_id, task_ids=task_ids), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):

    goal = validate_item(Goal, goal_id)
    tasks = goal.tasks

    tasks_to_dict = []
    tasks_to_dict = [task.to_dict() for task in tasks]

    return jsonify(id=goal.goal_id, title=goal.title, tasks=tasks_to_dict), 200