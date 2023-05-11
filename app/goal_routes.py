from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app.task_routes import validate_task

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"Goal {id} is invalid"}, 400))

    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message": f"Goal {id} not found"}, 404))

    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)

    new_goal = Goal(
        title = request_body["title"]
    )
    
    db.session.add(new_goal)
    db.session.commit()
    goal_dict = dict(goal=new_goal.to_dict())
    
    return make_response(jsonify(goal_dict), 201)

@goal_bp.route("", methods=["GET"])
def get_goals():
    sort = request.args.get("sort")
    
    if sort == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    else:
        goals = Goal.query.order_by(Goal.title.desc()).all()
    
    goals_list = []
    for goal in goals:
        goals_list.append(goal.to_dict())
    return jsonify(goals_list)

@goal_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goals = validate_goal(id)
    goal_dict = dict(goal=goals.to_dict())
    
    return make_response(jsonify(goal_dict), 200)

@goal_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    goal_data = request.get_json()
    
    goal.title = goal_data["title"]
    
    db.session.commit()
    
    goal_dict = dict(goal=goal.to_dict())
    return make_response(jsonify(goal_dict), 200)

@goal_bp.route("/<id>", methods=["DELETE"])
def delete_one_goal(id):
    goal = validate_goal(id)
    
    deleted_response = {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }
    
    db.session.delete(goal)
    db.session.commit()
    
    return make_response(jsonify(deleted_response), 200)

@goal_bp.route("/<id>/tasks", methods=["POST"])
def add_tasks_to_goal(id):
    goal = validate_goal(id)
    goal_data = request.get_json()
    task_ids = goal_data.get("task_ids", [])
    
    new_tasks = [validate_task(task_id) for task_id in task_ids]
    
    goal.tasks = new_tasks
    
    db.session.commit()
    
    updated_goal = validate_goal(id)
    
    return make_response(jsonify({"id": updated_goal.goal_id, "task_ids": task_ids}), 200)
    
@goal_bp.route("/<id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(id):
    goal = validate_goal(id)
    tasks = goal.tasks
    task_list = []
    
    for task in tasks:
        task_dict = task.to_dict()
        task_list.append(task_dict)
        
    return jsonify({"id": goal.goal_id,"tasks": task_list, "title": goal.title}), 200

@goal_bp.route("/<id>/tasks", methods=["GET"])
def get_goal_no_matching_tasks(id):
    goal = validate_goal(id)
    tasks = goal.tasks

    task_list = []
    for task in tasks:
        task_dict = task.to_dict()
        task_list.append(task_dict)

    response_data = {"goal_id": goal.goal_id, "tasks": task_list}
    return jsonify(response_data), 200

@goal_bp.route("/<id>/tasks", methods=["GET"])
def get_no_matching_goal_tasks(id):
    abort(404, description="Goal not found")
