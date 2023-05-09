from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db 


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# helper function to validate_task
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task


# Routes/Endpoints below 

# create one task
@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    # this try except also works!
    # try:
    #     new_task = Task(title=request_body["title"], description=request_body["description"])

    # except KeyError:
    #     return {"details": "Invalid data"}, 400


    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))
    else:
        new_task = Task(title=request_body["title"], 
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": new_task.to_dict()
    }

    return response_body, 201


# read/get all tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    sort_request_from_user = request.args.get("sort")
    tasks_response = []
    # if user passes in sort as query param, we must check if it is asc or desc
    if sort_request_from_user: 
        if sort_request_from_user == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        if sort_request_from_user == "desc":
            tasks = Task.query.order_by(Task.title.desc())

    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response), 200 


# read/get one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return {"task": task.to_dict()}, 200
    # returning as a dict here plus calling to_dict because it's a nested dictionary. If I updated to_dict to handle nested dictionaries it would no longer work for read_all_tasks


# update one task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    if request_body["title"]:
        task.title = request_body["title"]

    if request_body["description"]:
        task.description = request_body["description"]

    # come back to this!
    # eventually you will need this b/c you will need the option to update this attribute 
    # if request_body["completed_at"]:
    #     task.completed_at = request_body["completed_at"]

    db.session.add(task)
    db.session.commit()

    response_body = {
        "task": task.to_dict()
    }

    return response_body, 200 


# delete one task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }), 200)


