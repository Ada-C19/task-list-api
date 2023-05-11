from flask import Blueprint, jsonify, abort, make_response, request
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

        message = Task.generate_message(new_task)

        return make_response(jsonify(message), 201)
    except KeyError as e:
        message = f"Invalid request. Missing required value: {e}"
        return make_response({"details": message}, 400)

    # except KeyError as e:
    #     abort(make_response(f"Invalid request. Missing required value: {e}", 400))

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

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_planet(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.update(request_body)

    db.session.commit()
    message = Task.generate_message(task)
    return make_response(jsonify(message))
          
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    message = {
        "details": f"Task {task_id} \"{task.description}\" successfully deleted"
        }
    return make_response(jsonify(message), 200)

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        message = f"{cls.__name__} {id} is invalid"
        abort(make_response({"message": message}, 400))

    obj = cls.query.get(id)
    if not obj:
        abort(make_response(jsonify(message=f"{cls.__name__} not found"), 404))
    
    return obj
