from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        message = f"{cls.__name__} {model_id} invalid"
        abort(make_response({"error": message}, 400))

    model = cls.query.get(model_id)

    if not model:
        message = f"{cls.__name__} #{model_id} not found"
        abort(make_response({"error": message}, 404))

    return model

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try: 
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()
        return make_response({"task": new_task.to_dict()}, 201)
    except:
        return make_response({"details": "Invalid data"}, 400)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else: 
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = validate_model(Task, task_id)
    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    task_data = request.get_json()

    task.title = task_data["title"]
    task.description = task_data["description"]

    db.session.commit()
    
    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    details = f"Task {task.task_id} \"{task.title}\" successfully deleted"
    return make_response({"details": details}, 200)