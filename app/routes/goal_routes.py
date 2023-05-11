from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, abort, request
from app.helper_functions import validate_model, create_slack_message



goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        goal = Goal.from_dict(request_body)
        db.session.add(goal)
        db.session.commit()

        return make_response({"goal": goal.to_dict()}, 201)

    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    title_query = request.args.get("sort")
    if title_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif title_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    try:
        goal.title = request_body["title"]
        db.session.commit()

        return make_response({"goal": goal.to_dict()}, 200)
    
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    try:
        tasks_list = request_body["task_ids"]
        for task in tasks_list:
            new_task = validate_model(Task, task)
            new_task.goal_id = goal.goal_id
        
        db.session.commit()

        task_id_list = []
        for task in goal.tasks:
            task_id_list.append(task.task_id)

        return make_response({"id": goal.goal_id, "task_ids": task_id_list}, 200)

    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_one_goals_task(goal_id):
    goal = validate_model(Goal, goal_id)
    
    task_response = []
    for task in goal.tasks:
        task_response.append(task.to_dict())

    return_dict = goal.to_dict()
    return_dict["tasks"] = task_response
    return make_response(return_dict, 200)


    


  