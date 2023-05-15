from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response, abort 

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError as err:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    goal_dict = {}
    goal_dict["goal"] = new_goal.to_dict()

    return jsonify(goal_dict), 201


@goals_bp.route("", methods=["GET"])
def sort_by_title():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(Goal.title)
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    
    goal_response = [goal.to_dict() for goal in goals]
    
    return jsonify(goal_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_dict = {"goal": goal.to_dict()}

    return jsonify(goal_dict)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    goal_dict = {"goal": goal.to_dict()}

    return jsonify(goal_dict)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    goal_message = {"details": f'Goal {goal.goal_id} \"{goal.title}\" successfully deleted'}

    return jsonify(goal_message)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_response = goal.to_dict(tasks=True)
    return make_response(goal_response), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    for task in goal.tasks:
        task.goal_id = None


    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.goal_id

    goal.title = request.args.get("title", goal.title)
    
    db.session.commit()

    return make_response({"id": goal.goal_id, "task_ids": task_ids}, 200)