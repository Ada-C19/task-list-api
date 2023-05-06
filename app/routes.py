from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import datetime
from sqlalchemy.orm.exc import NoResultFound


bp = Blueprint("bp", __name__, url_prefix="/tasks")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


@bp.route("", methods=["POST"])
def creat_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }), 201)


@bp.route("", methods=["GET"])
def read_all_tasks():
    task_query = Task.query
    title_query = request.args.get("sort")

    if title_query == "asc":
        task_query = Task.query.order_by(Task.title.asc())
    if title_query == "desc":
        task_query = Task.query.order_by(Task.title.desc())

    tasks = task_query.all()
    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())

    return jsonify(task_response)


@bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify({"task": task.to_dict()}), 200


@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"],
    task.description = request_body["description"],
    task.is_complete = False

    db.session.commit()

    return make_response(jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }), 200)


@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task 1 \"{task.title}\" successfully deleted"})), 200

@bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    try:
        task = validate_model(Task, task_id)
    except NoResultFound:
        return make_response(jsonify({"error": "Task not found"}), 404)
    
    if task.completed_at is None:
        task.completed_at = datetime.datetime.now()
        db.session.commit()
    
    task_data = task.to_dict()
    if task.completed_at:
        task_data["completed_at"] = task.completed_at.strftime('%m-%d-%Y')

    task_data.pop("completed_at", None)
    
    return make_response(jsonify({
        "task": task_data
    }), 200)

@bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    try:
        task = validate_model(Task, task_id)
    except NoResultFound:
        return make_response(jsonify({"error": "Task not found"}), 404)
    
    if task.completed_at is not None:
        task.completed_at = None
        db.session.commit()
    
    task_data = task.to_dict()

    task_data.pop("completed_at", None)
    
    return make_response(jsonify({
        "task": task_data
    }), 200)