from app import db
from .tasks_routes import validate_model
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request

goals_bp = Blueprint("goals_bp",__name__, url_prefix="/goals")

@goals_bp.route("",methods=["POST"])
def create_goal_2():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except:
        return {"details": "Invalid data"} , 400
    
    db.session.add(new_goal)
    db.session.commit()

    return {"goal":{
                "id": new_goal.goal_id,
                "title": new_goal.title
            }}, 201


@goals_bp.route("",methods=["GET"])
def read_all_goals():

    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_task(goal_id):
    goal = validate_model(Goal, goal_id)

    return {
        "goal":{
        "id": goal.goal_id,
        "title": goal.title}}, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal_to_update = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal_to_update.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal":goal_to_update.to_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return abort(make_response({"details":f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200))


#RELATIONSHIP
#Goals(parent) with tasks(child)
#Como usuario, quiero agregar tasks a un goal
@goals_bp.route("/<goal_id>/tasks",methods=["POST"])
def create_goal(goal_id):

    goal_from_id = validate_model(Goal, goal_id)

    request_body = request.get_json()
    for i in request_body["task_ids"]:
        task_to_update = validate_model(Task, i)
        task_to_update.goal = goal_from_id
        db.session.commit()

    return make_response(jsonify({
                "id": int(goal_id),
                "task_ids":request_body["task_ids"]
            })), 200



