from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app.task_routes import validate_task
from app import db

goal_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"Goal {goal_id} invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    
    if not goal:
        abort(make_response({"message":f"Goal {goal_id} not found"}, 404))
    return goal if goal else abort(make_response({"message":f"Goal {goal_id} not found"}, 404))

#CREATE GOALS

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal(goal_id):
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
        new_goal.description == "Test Description"
        new_goal.completed_at == None
    except:    
        abort(make_response({f"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()
    
    return make_response({f"goal":new_goal.to_dict()}, 201)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_in_goal(goal_id):

    goal = validate_goal(goal_id)
    task_ids = request.json.get("task_ids", [])

    for task_id in task_ids:
        task = validate_task(task_id)
        task.goal_id = goal_id
    db.session.commit()

    return make_response({f"id": int(goal_id), "task_ids": task_ids}, 200)

#READ GOALS

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    title_query = request.args.get("sort")
    if title_query:
        if title_query == "asc":
            goals = Goal.query.order_by(Goal.title.asc())
        elif title_query == "desc":
            goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()

    goals_response = [Goal.to_dict(goal) for goal in goals]

    return make_response((goals_response), 200)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return make_response({"goal": goal.to_dict_with_task()}, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_task(goal_id):
    goal = validate_goal(goal_id)
    goals_response = goal.to_dict_with_tasks()
    return make_response({goals_response}, 200)

#UPDATE GOALS

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()
    
    return make_response({f"goal": goal.to_dict()}, 200)

# DELETE GOALS

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({f"details":f"Goal {goal_id} \"{goal.title}\" successfully deleted"})