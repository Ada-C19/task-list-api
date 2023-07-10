from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, abort, make_response, request, jsonify

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"goal {goal_id} is invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    
    if not goal:
        abort(make_response({"details": f"Goal {goal_id} not found"}, 404))
    
    return goal

def validate_task_list(task_ids):
    try:
        task_ids = list(task_ids)
    except:
        abort(make_response({"message": f"task_ids list {task_ids} is invalid"}, 400))
    
    task_list = []
    
    for task_id in task_ids:
        task = Task.query.get(task_id)
        if not task:
            abort(make_response({"details": f"Task {task_id} not found"}))
        task_list.append(task)
    
    return task_list

# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"message": f"task {task_id} is invalid"}, 400))

#     task = Task.query.get(task_id)
    
#     if not task:
#         abort(make_response({"details": f"Task {task_id} not found"}, 404))
    
#     return task
    

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))
    
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()
    
    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201

@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return jsonify(goals_response)

# Get one saved goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    
    return {"goal": goal.to_dict()}

# Update goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    
    request_body = request.get_json()
    
    if "title" not in request_body:
        abort(make_response({"details": f"Missing title"}, 400))
    
    goal.title = request_body["title"]
    
    db.session.commit()
    
    return make_response({"goal": {"id": goal.goal_id, "title": goal.title}})

# Delete goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return make_response({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})

# Send a list of Task IDs to a goal
@goals_bp.route("/<goal_id>/tasks", methods=[])
def add_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    
    request_body = request.get_json()
    
    tasks = validate_task_list(request_body("task_ids"))
    
    for task in tasks:
        