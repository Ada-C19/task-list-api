from app import db 
from app.models.goal import Goal 
from app.models.task import Task
from flask import Blueprint, make_response, request, jsonify, abort

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal(): 
    request_body = request.get_json()

    if "title" not in request_body: 
        return make_response({"details" : "Invalid data"}, 400)

    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def link_task_ids_to_goal(goal_id):
    goal =validate_item(Goal, goal_id)

    request_body = request.get_json() 

    ids = request_body["task_ids"]
    for task_id in ids: 
        one_task =validate_item(Task,task_id)
        one_task.goal = goal 
        db.session.add(one_task) 

    db.session.commit()

    result = {
        "id": goal.id,
        "task_ids" :ids}
    
    return jsonify(result), 200

@goal_bp.route("", methods=["GET"])
def read_all_goals(): 
    response = []

    all_goals = Goal.query.all()

    for goal in all_goals: 
        response.append(goal.to_dict())
    
    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id): 
    goal = validate_item(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200 

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id): 
    goal = validate_item(Goal, goal_id)

    tasks = [task.to_dict() for task in goal.tasks]

    result = goal.to_dict()
    result['tasks'] = tasks

    return jsonify(result), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id): 
    goal = validate_item(Goal, goal_id)

    request_data = request.get_json()

    goal.title = request_data["title"]
    
    db.session.commit()

    return {"goal": goal.to_dict()}, 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id): 
    goal = validate_item(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200

def validate_item(model, item_id):
    try: 
        item_id = int(item_id)
    except ValueError: 
        return abort(make_response({"msg": f"invalid id: {item_id}"}, 400))
    
    model = model.query.get(item_id)

    if not model: 
        abort(make_response({"msg": f"{item_id} not found"}, 404))
    
    return model 