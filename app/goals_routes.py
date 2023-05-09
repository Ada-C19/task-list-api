from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from app.tasks_routes import validate_task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"Goal {id} is invalid"}, 400))

    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"message": f"Goal {id} not found"}, 404))

    return goal

# WAVE 5: Create a Goal: Valid Goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
        
    new_goal = Goal(
        title = request_body["title"],
    )

    db.session.add(new_goal)
    db.session.commit()
    goal_dict = dict(goal=new_goal.make_goal_dict())

    return make_response(jsonify(goal_dict), 201)

# WAVE 5: Get Goals: Getting Saved Goals
# WAVE 5: Get Goals: No Saved Goals
# WAVE 5: Get One Goal: One Saved Goal
@goals_bp.route("", methods=["GET"])
def get_all_saved_goals():
    goals = Goal.query.all()
    goals_list = []
    for goal in goals:
        goals_list.append(goal.make_goal_dict())

    goals_list = [goal.make_goal_dict() for goal in goals] 

    return jsonify(goals_list), 200 

# WAVE 5: Get One Goal: One Saved Goal cont.
@goals_bp.route("/<id>", methods=["GET"])
def get_one_saved_goal(id):
    goal = validate_goal(id)

    goal_dict = dict(goal=goal.make_goal_dict())

    return make_response(jsonify(goal_dict), 200)

# WAVE 5: Update Goal
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    goal_dict = dict(goal=goal.make_goal_dict())
    return make_response(jsonify(goal_dict), 200)

# WAVE 5: Delete Goal: Deleting a Goal
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)

    deleted_response = {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify(deleted_response), 200)

# WAVE 6: Sending a List of Task IDs to a Goal
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    for id in task_ids:
        task = validate_task(id)
        task.goal_id = goal_id

    goal_dict = dict(id=int(task.goal_id), task_ids=task_ids)

    db.session.add(task)
    db.session.commit()

    return make_response(jsonify(goal_dict), 200)


# WAVE 6: Getting Tasks of One Goal
# WAVE 6: Getting Tasks of One Goal: No Matching Tasks
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_one_goals_tasks(goal_id):
    goal = validate_goal(goal_id)
    
    tasks_response = []
    for task in goal.tasks:
        new_task_dict = task.make_task_dict()
        tasks_response.append(new_task_dict)

    goal_dict = goal.make_goal_dict()
    goal_dict["tasks"] = tasks_response
    
    return make_response(jsonify(goal_dict), 200)



