from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.task_routes import validate_model
from flask import Blueprint, jsonify, abort, make_response, request

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# def validate_model(cls, model_id):
#     try:
#         model_id = int(model_id)
#     except:
#      abort(make_response({"details":"Invalid data"}, 400))

#     model = cls.query.get(model_id)

#     if not model:
#         abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

#     return model

@goal_bp.route("", methods=["POST"])
def creat_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({
        "goal": {
            "id" : new_goal.goal_id,
            "title" : new_goal.title
        }
    }), 201)

@goal_bp.route("", methods=["GET"])
def read_all_goal():
    title_query = request.args.get("title")

    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    else:
        goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({"goal": goal.to_dict()}), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({
        "goal": {
            "id" : goal.goal_id,
            "title" : goal.title
        }
    }), 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal 1 \"{goal.title}\" successfully deleted"})), 200

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):

    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    task_ids= request_body["task_ids"]

    new_task_ids = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal_id
        new_task_ids.append(task.task_id)
        
        db.session.commit()

    goal.task_ids = new_task_ids
    db.session.commit()
    
    return jsonify({"id": goal.goal_id, 
                    "task_ids": new_task_ids}), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_task_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks = Task.query.filter(Task.goal_id == goal.goal_id)

    task_dicts = []
    for task in tasks:
        task_dict = {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
        task_dicts.append(task_dict)

    return make_response(jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_dicts
    }))
