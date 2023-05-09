from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db
from .task import validate_task


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


# Helper function
def get_valid_goal_by_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    goal = Goal.query.get(goal_id)

    return goal if goal else abort(make_response({'msg': f"No goal with id {goal_id}"}, 404))


# Routes
@goals_bp.route("", methods=['POST'])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return {
            "details": "Invalid data"
            }, 400

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route("", methods=['GET'])
def handle_goals():
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    elif sort_query == "asc":
        goals = Goal.query.order_by(Goal.title)
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=['GET'])
def handle_goal(goal_id):
    goal = get_valid_goal_by_id(goal_id)
    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_one_goal(goal_id):
    request_body = request.get_json()

    goal_to_update = get_valid_goal_by_id(goal_id)
    goal_to_update.title = request_body["title"]

    db.session.commit()

    return {"goal": goal_to_update.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_one_goal(goal_id):
    goal_to_delete = get_valid_goal_by_id(goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    return {
        "details":
            f'Goal {goal_to_delete.goal_id} "{goal_to_delete.title}" successfully deleted'
        }, 200


@goals_bp.route("/<goal_id>/tasks", methods=['POST'])
def post_task_ids_to_goal(goal_id):
    goal = get_valid_goal_by_id(goal_id)

    request_body = request.get_json()
    # Get the task ids from the request body
    task_ids = request_body["task_ids"]

    # Get the Task instances (task dicts) based on the task ids
    task_instances = [validate_task(task_id) for task_id in task_ids]
    goal.tasks.extend(task_instances)

    db.session.commit()

    return {
        "id": goal.to_dict()["id"],
        "task_ids": task_ids
    }, 200


@goals_bp.route("/<goal_id>/tasks", methods=['GET'])
def get_tasks_for_one_goal(goal_id):
    goal = get_valid_goal_by_id(goal_id)
    
    # Get task dicts and append them to `tasks` list
    tasks = [task.to_dict() for task in goal.tasks]

    goal_dict = goal.to_dict()

    # Add `tasks` list to the key "tasks" 
    goal_dict["tasks"] = tasks

    return goal_dict, 200


