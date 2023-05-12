from app import db
from flask import Blueprint, jsonify, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app.helper_functions import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    
    title_query = request.args.get("title")
    if title_query:
        goals = Goal.query.filter_by(title=title_query)

    if request.args.get("sort") == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()

    elif request.args.get("sort") == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
        
    else:
        goals = Goal.query.all()
        
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())
    return jsonify(goals_response), 200

#GET route to read one task
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_task(goal_id):
    goal = validate_model(Goal,goal_id)
    return jsonify({"goal": goal.to_json()}), 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal":new_goal.to_json()}), 201

#UPDATE route to edit a goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal": goal.to_json()}), 200

#DELETE existing goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})


#POST ROUTE
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def link_tasks_to_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal_id = goal_id
        db.session.add(task)
    
    db.session.commit()

    return make_response({"id": goal.goal_id, "task_ids":request_body["task_ids"]}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_goal_tasks(goal_id):

    goal = validate_model(Goal, goal_id)

    return jsonify(goal.to_json()), 200
