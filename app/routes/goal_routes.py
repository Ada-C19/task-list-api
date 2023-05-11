from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

goal_list_bp = Blueprint("goal_list_bp", __name__, url_prefix="/goals")

# Create new goal
@goal_list_bp.route("", methods=["POST"])
def create_goal():
    # get request data
    request_body = request.get_json()
    
    # return 400 message if title doesn't exist in request data
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    # create new goal if title exists in request data
    new_goal = Goal(title=request_body["title"])
    
    # add and commit new goal
    db.session.add(new_goal)
    db.session.commit()
    
    # return dict of goal dicts
    return {"goal": new_goal.to_dict() }, 201
    
# Get all saved goals or zero saved goals
@goal_list_bp.route("", methods=["GET"])
def get_goals():
    # get all goals
    goals = Goal.query.all()
    
    # initialize list of goals
    goals_response = []
    
    # loop thru each goal
    for goal in goals:
        # return goal dictionary and add it to list
        goals_response.append(goal.to_dict())
    
    # return list of goal dicts if they exist or return empty list if no goals    
    return jsonify(goals_response)

# Get one goal
@goal_list_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    # return goal if goal_id valid and exists
    goal = validate_item(Goal, goal_id)
    
    # return dict of goal dicts
    return {"goal": goal.to_dict()}
    
# Update goal
@goal_list_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    # return goal if goal_id valid and exists
    goal = validate_item(Goal, goal_id)
    
    # get request data
    request_data = request.get_json()
    
    # update goal w/ new title
    goal.title = request_data["title"]
    
    # commit updated goal
    db.session.commit()
    
    # return dict of goal dicts
    return {"goal": goal.to_dict()}
    
# Delete goal
@goal_list_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    # return goal if goal_id valid and exists
    goal = validate_item(Goal, goal_id)
    
    # delete goal and commit delete
    db.session.delete(goal)
    db.session.commit()
    
    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}

# Associate tasks w/ goal
@goal_list_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    # return goal if goal_id valid and exists
    goal = validate_item(Goal, goal_id)

    # get request data
    request_body = request.get_json()
    # request_body is a dict
    
    # pull out list of task IDs
    task_ids_list = request_body["task_ids"]
    
    # loop thru each task ID
    for task_id in task_ids_list:
        # return task if task_id valid and exists
        task = validate_item(Task, task_id)
        
        # attach task to goal
        task.goal = goal
        
        # commit task attached to goal                 
        db.session.commit()
    
    return {"id": goal.goal_id,
            "task_ids": task_ids_list}

# Get tasks of goal
# Get tasks of goal: No Matching Tasks
# Get tasks of goal: No Matching Goal
@goal_list_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    # return goal if goal_id valid and exists
    goal = validate_item(Goal, goal_id)
    
    # initialize list of tasks
    tasks_response = []
    #jsonify(tasks_response)
    
    # loop thru each task associated with given goal 
    for task in goal.tasks:
        # return task dictionary
        task_with_goal = task.to_dict()
        # add goal_id:value pair to task dictionary
        task_with_goal["goal_id"] = goal.goal_id
        # add task dictionary to list
        tasks_response.append(task_with_goal)

    # return goal dictionary
    goal_with_tasks = goal.to_dict()
    # add tasks:value pair to goal dictionary
    goal_with_tasks["tasks"] = tasks_response
    
    # return goal dict w/ task dicts
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