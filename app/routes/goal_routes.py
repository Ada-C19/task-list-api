from app import db
from app.models.goal import Goal 
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

'''
Goal CRUD Routes
'''
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    else:
        new_goal = Goal(title = request_body["title"])
                    
    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": {"id": new_goal.id, "title": new_goal.title,}}, 201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.id,
            "title": goal.title})
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):    
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({"message" :f"Goal {goal_id} not found"}, 404)
    return make_response({"goal": {"id": goal.id, "title": goal.title}}, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({'message': f'Goal {goal_id} not found'}, 404)

    form_data = request.get_json()
    goal.title = form_data["title"]

    db.session.commit()
    return make_response({"goal": {"id": goal.id, "title": goal.title}}, 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response({'message': f'Goal {goal_id} not found'}, 404)
    
    db.session.delete(goal)
    db.session.commit()

    return make_response({'details' : f'Goal {goal_id} "{goal.title}" successfully deleted'})

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal is None:
        return make_response({'message': f'Goal {goal_id} not found'}, 404)
    tasks = Task.query.join(Goal).filter(Task.goal_id == goal_id).all()
    task_list = []
    if tasks:
        for task in tasks:
            task_list.append(task.response_dict())

    if request.method == "GET":
        return make_response({
                "id": goal.id,
                "title": goal.title,
                "tasks": task_list 
        }, 200)
    
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_for_goal(goal_id):
        goal = Goal.query.get(goal_id)
    
        if goal is None:
            return make_response({'message': f'Goal {goal_id} not found'}, 404)
        tasks = Task.query.join(Goal).filter(Task.goal_id == goal_id).all()
        task_list = []
        if tasks:
            for task in tasks:
                task_list.append(task.response_dict())

        form_data = request.get_json()
        goal.tasks = []

        task_ids = form_data["task_ids"]
        for task_id in task_ids:
            task = Task.query.get(task_id)
            goal.tasks.append(task)

        db.session.commit()

        return make_response({
            "id": goal.id, 
            "task_ids": task_ids
        }, 200)