from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

goal_list_bp = Blueprint("goal_list_bp", __name__, url_prefix="/goals")

# Create new goal
@goal_list_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()
    
    return {"goal": new_goal.to_dict() }, 201
    
# Get all saved goals or zero saved goals
@goal_list_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    
    for goal in goals:
        goals_response.append(goal.to_dict())
        
    return jsonify(goals_response)

# Get one goal
@goal_list_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    return {"goal": goal.to_dict()}
    
# Update goal
@goal_list_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    request_data = request.get_json()
    
    goal.title = request_data["title"]
    
    db.session.commit()
    
    return {"goal": goal.to_dict()}
    
# Delete goal
@goal_list_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}

# Associate tasks w/ goal
@goal_list_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate_item(Goal, goal_id)

    request_body = request.get_json()
    # request_body is a dict
    
    # pull out list of task IDs
    task_ids_list = request_body["task_ids"]
    
    for task_id in task_ids_list:
        task = Task.query.get(task_id)
        if not task:
            new_task = Task(task_id=task_id, 
                            goal=goal)
            db.session.add(new_task)
            
        task.goal = goal
                        
        db.session.commit()
    
    return {"id": goal.goal_id,
            "task_ids": task_ids_list}

# Get tasks of goal
# Get tasks of goal: No Matching Tasks
# Get tasks of goal: No Matching Goal
@goal_list_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    # Ask instructor how to jsonify this list w/o causing errors???
    tasks_response = []
    jsonify(tasks_response)
    
    for task in goal.tasks:
        task_with_goal = task.to_dict()
        task_with_goal["goal_id"] = goal.goal_id
        tasks_response.append(task_with_goal)

    goal_with_tasks = goal.to_dict()
    goal_with_tasks["tasks"] = tasks_response
    
    return goal_with_tasks

# No matching Goal or Task: Get, Update, and Delete
# Helper function
def validate_item (model, item_id):
    try:
        item_id_int = int(item_id)
    except:
        return abort(make_response({"message":f"Item {item_id} invalid"}, 400))
    
    item = model.query.get(item_id_int)
    
    if not item:
        return abort(make_response({"message":f"Item {item_id_int} not found"}, 404))
    
    return item    