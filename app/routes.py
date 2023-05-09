from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from app.helper import validate_task

tasks_bp = Blueprint("tasks", __name__, url_prefix= "/tasks") 

# GET all task - GET[READ] - /tasks

@tasks_bp.route("", methods =["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_query = request.args.get("is_complete")

    if title_query:
        tasks = Task.query.filter_by(title = title_query)
    elif description_query:
        tasks = Task.query.filter_by(description = description_query)
    elif completed_query:
        tasks = Task.query.filter_by(is_completed = completed_query)
    else:
        tasks = Task.query.all()


    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200

# GET one task - /tasks/<id>  - [READ]

@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return jsonify({"task":task.to_json()}), 200

#POST  - /tasks - [CREATE]
@tasks_bp.route("", methods= ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.create_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":new_task.to_json()}), 201