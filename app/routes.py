from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from sqlalchemy import asc, desc
from datetime import timezone, datetime
from pytz import utc

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

NOWTIME = datetime.now(timezone.utc)

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

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