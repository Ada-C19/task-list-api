from flask import Blueprint,make_response,request,jsonify,abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.helper import validate_goal,validate_task


#CREATE BP/ENDPOINT
goals_bp = Blueprint("goals",__name__, url_prefix="/goals")


#POST request/response [POST]/goals :(CREATE)
@goals_bp.route("",methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        # if "title" in request_body:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return make_response({"details": "Invalid data"},400)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.to_dict()}),201


#GET one goal [GET]/goals/<id> :(CREATE)
@goals_bp.route("/<id>",methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)

    return jsonify({"goal":goal.to_dict()}),200


#GET all goals [GET]/goals  :(CREATE)
@goals_bp.route("",methods=["GET"])
def get_all_goals():
    goals_response = []
    goals = Goal.query.all()

    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return jsonify(goals_response),200


#UPDATE one task [PUT]/goals/<id> :(UPDATE)
@goals_bp.route("/<id>",methods=["PUT"])
def update_goal(id):
    goal = Goal.query.get(id)
    if goal is None:
        return jsonify({"error": "Goal not found"}),404
    
    request_body = request.get_json()
    goal.update_goal(request_body)
    db.session.commit()

    return jsonify({"goal":goal.to_dict()}),200


#DELETE one goal [DELETE]/goals/<id> :(DELETE)
@goals_bp.route("/<id>",methods=["DELETE"])
def delete_goal(id):
    goal_to_delete = validate_goal(id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    message = {'details': f'Goal {id} "{goal_to_delete.title}" successfully deleted'}

    return make_response(message,200)

#-----------------------------------------------
#CREATE task by goal  [POST]/<goal_id_parent>/tasks - :(CREATE)
@goals_bp.route("/<goal_id_parent>/tasks",methods=["POST"])
def create_task(goal_id_parent):
    goal = validate_goal(goal_id_parent)
    request_body = request.get_json()

    tasks_list_dict = request_body
    for task_id in tasks_list_dict["task_ids"]:
        task = validate_task(task_id)
        task.goal = goal
    
    db.session.commit()
    result=dict(id=goal.goal_id,
                task_ids=tasks_list_dict["task_ids"])
    
    return make_response(jsonify(result),200)


#GET all tasks by goal [GET]/<goal_id_parent>/tasks - :(READ)
@goals_bp.route("/<goal_id_parent>/tasks",methods=["GET"])
def handle_tasks_from_goal(goal_id_parent):
    goal = validate_goal(goal_id_parent)
    tasks = goal.tasks
    tasks_lists = [validate_task(task.task_id).to_dict() for task in tasks]

    for task_dict in tasks_lists:
        task_dict["goal_id"]=int(goal_id_parent)
    
    result = dict(id=goal.goal_id,
                  title=goal.title,
                  tasks=tasks_lists)
    
    return make_response(jsonify(result),200)
