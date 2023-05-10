from flask import Blueprint, jsonify, abort, make_response, request, Response
from app import db
from app.models.task import Task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()
    try:
        new_task = Task.create_new_task(request_body)
        db.session.add(new_task)
        db.session.commit()

        message = f"Task {new_task.task_title} successfully created"
        return make_response(jsonify(message), 201)

    except KeyError as e:
        abort(make_response(f"Invalid request. Missing required value: {e}", 400))



@tasks_bp.route("", methods = ["GET"])
def read_all_tasks():
    tasks_response = []
    query_params = request.args.to_dict()

    if query_params:
        query_params = {k.lower(): v.title() for k, v in query_params.items()}
        tasks = Task.query.filter_by(**query_params).all()
    else:
        tasks = Task.query.all()

    tasks_response = [task.task_to_dict() for task in tasks]
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    task = Task.query.get(task_id)
    return jsonify(task.task_to_dict()), 200

def validate_model(cls, id):
     try:
         id = int(id)
     except:
         message = f"{cls.__name__} {id} is invalid"
         abort(make_response({"message": message}, 400))