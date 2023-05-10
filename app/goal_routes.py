from flask import Blueprint, request, abort, make_response, jsonify
from app.models.goal import Goal
from app.models.task import Task
from app import db
from .task_routes import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# Create
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    check_goal_data(request_body)

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)
    

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_ids = request.json.get("task_ids")
    tasks = Task.query.filter(Task.id.in_(task_ids)).all()

    for task in tasks:
        goal.tasks.append(task)
    
    db.session.commit()

    return make_response({
                            "id": int(goal_id),
                            "task_ids": task_ids
                        })


# Read
@goals_bp.route("", methods=["GET"])
def list_all_goals():
    goals_response = []
    goals = Goal.query.all()
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def list_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response({"goal": goal.to_dict()})


@goals_bp.route("<goal_id>/tasks", methods=["GET"])
def list_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_list = [task.to_dict() for task in goal.tasks]
    for task in task_list:
        task["goal_id"] = goal.id
    return make_response({
                            "id": goal.id,
                            "title": goal.title,
                            "tasks": task_list
                        })
            

# Update
@goals_bp.route("<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal": goal.to_dict()})


# Delete
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"})







# Helper Functions
def check_goal_data(request):
    if "title" not in request:
        return abort(make_response({"details": "Invalid data"}, 400))