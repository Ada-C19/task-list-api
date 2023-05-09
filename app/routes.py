from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from sqlalchemy import asc, desc
from datetime import timezone, datetime
from pytz import utc

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

NOWTIME = datetime.now(timezone.utc)

def get_task_instance(request):
        task_info = validate_data(request)
        return Task(
                title = task_info["title"],
                description = task_info["description"],
                completed_at = task_info["completed_at"]
    )

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Invalid task ID: {task_id}"}, 400))
    print(f"{task_id = }")
    return task_id

def get_task_by_id(task_id):
    task_id = validate_task_id(task_id)
    task = db.session.get(Task, task_id)

    if not task:
        abort(make_response({'message': f'Task {task_id} was not found.'}, 404))
        
    return task 

def update_task_from_request(task, request):
    task_info = request.get_json()

        # now = datetime.now(timezone.utc)

    if 'title' in task_info:
        task.title = task_info['title']
    if 'description' in task_info:
        task.description = task_info['description']
    # if 'completed_at' in task_info:
    #     task.completed_at = task_info['completed_at']

    # task.title = task_info["title"],
    # task.description = task_info["description"],
    task.completed_at = None

    return task

def validate_data(request):
    task_info = request.get_json()
    if not "title" in task_info or not "description" in task_info:
        abort(make_response({"details": "Invalid data"}, 400))
    if not "completed_at" in task_info:
        task_info["completed_at"] = None
    return task_info

# def validate_data(request):
#     task_info = request.get_json()
#     if "title" not in task_info or "description" not in task_info or "completed_at" not in task_info:
#         abort(make_response({"details": "Invalid data"}, 400))

#     return task_info


@tasks_bp.route("", methods=['POST'])
def create_task():
    new_task = get_task_instance(request)

    db.session.add(new_task)
    db.session.commit()

    task = new_task.to_json()

    return make_response(jsonify(task=task)), 201

# @tasks_bp.route("", methods=['GET'])
# def get_tasks():
#     tasks = Task.query.all()

#     task_list = [task.to_json() for task in tasks]

#     return jsonify(task_list), 200

@tasks_bp.route("", methods=['GET'])
def get_tasks():
    sort_order = request.args.get("sort", None)

    tasks = Task.query

    title_query = request.args.get("title")
    if title_query:
        tasks = tasks.filter_by(title=title_query)

    if sort_order == "asc":
        tasks = tasks.order_by(asc(Task.title))
    elif sort_order == "desc":
        tasks = tasks.order_by(desc(Task.title))

    tasks = tasks.all()

    task_list = [task.to_json() for task in tasks]

    return jsonify(task_list), 200

@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = get_task_by_id(task_id)
    return make_response(jsonify({"task": task.to_json()})), 200

@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    task = get_task_by_id(task_id)
    updated_task = update_task_from_request(task, request)

    db.session.commit()

    task = updated_task.to_json()

    return make_response(jsonify(task=task)), 200

@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = get_task_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    message = f'Task {task_id} "{task.title}" successfully deleted'

    return make_response({"details" : message}), 200





# def update_task_from_request(task, request):
#     task_info = request.get_json()

#     if 'title' in task_info:
#         task.title = task_info['title']
#     if 'description' in task_info:
#         task.description = task_info['description']
#     if 'completed_at' in task_info:
#         task.completed_at = datetime.fromisoformat(task_info['completed_at'])

#     return task

@tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def mark_task_completed(task_id):
    task = get_task_by_id(task_id)

    task.completed_at = NOWTIME

    db.session.commit()

    task = task.to_json()
    task["is_complete"] = True

    return make_response(jsonify(task=task)), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = get_task_by_id(task_id)

    task.completed_at = None

    db.session.commit()

    task = task.to_json()
    task["is_complete"] = False

    return make_response(jsonify(task=task)), 200


# @tasks_bp.errorhandler(404)
# def handle_task_not_found(error):
#     return make_response(jsonify({"message": "Task not found."})), 404








# ________________

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')


def get_goal_instance(request):
        goal_info = validate_goal_data(request)
        return Goal(
                title = goal_info["title"],
                # description = goal_info["description"],
                # completed_at = goal_info["completed_at"]
    )

def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Invalid goal ID: {goal_id}"}, 400))

    return goal_id

def get_goal_by_id(goal_id):
    goal_id = validate_goal_id(goal_id)
    goal = db.session.get(Goal, goal_id)

    if not goal:
        abort(make_response({'message': f'Goal {goal_id} was not found.'}, 404))
        
    return goal 

def update_goal_from_request(goal, request):
    goal_info = request.get_json()

    if 'title' in goal_info:
        goal.title = goal_info['title']
    # if 'description' in goal_info:
    #     goal.description = goal_info['description']
    # goal.completed_at = None

    return goal

def validate_goal_data(request):
    goal_info = request.get_json()
    if not "title" in goal_info:
        abort(make_response({"details": "Invalid data"}, 400))
    # if not "completed_at" in goal_info:
    #     goal_info["completed_at"] = None
    return goal_info

@goals_bp.route("", methods=['POST'])
def create_goal():
    new_goal = get_goal_instance(request)

    db.session.add(new_goal)
    db.session.commit()

    goal = new_goal.to_json()

    return make_response(jsonify(goal=goal)), 201

@goals_bp.route("", methods=['GET'])
def get_goals():
    sort_order = request.args.get("sort", None)

    goals = Goal.query

    title_query = request.args.get("title")
    if title_query:
        goals = goals.filter_by(title=title_query)

    if sort_order == "asc":
        goals = goals.order_by(asc(Goal.title))
    elif sort_order == "desc":
        goals = goals.order_by(desc(Goal.title))

    goals = goals.all()

    goal_list = [goal.to_json() for goal in goals]

    return jsonify(goal_list), 200

@goals_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    goal = get_goal_by_id(goal_id)
    return make_response(jsonify({"goal": goal.to_json()})), 200

@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):
    goal = get_goal_by_id(goal_id)
    updated_goal = update_goal_from_request(goal, request)

    db.session.commit()

    goal = updated_goal.to_json()

    return make_response(jsonify(goal=goal)), 200

@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_goal(goal_id):
    goal = get_goal_by_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    message = f'Goal {goal_id} "{goal.title}" successfully deleted'

    return make_response({"details": message}), 200

@goals_bp.route("/<goal_id>/mark_complete", methods=['PATCH'])
def mark_goal_completed(goal_id):
    goal = get_goal_by_id(goal_id)

    goal.completed_at = NOWTIME

    db.session.commit()

    goal = goal.to_json()
    goal["is_complete"] = True

    return make_response(jsonify(goal=goal)), 200


@goals_bp.route("/<goal_id>/mark_incomplete", methods=['PATCH'])
def mark_goal_incomplete(goal_id):
    goal = get_goal_by_id(goal_id)

    goal.completed_at = None

    db.session.commit()

    goal = goal.to_json()
    goal["is_complete"] = False

    return make_response(jsonify(goal=goal)), 200