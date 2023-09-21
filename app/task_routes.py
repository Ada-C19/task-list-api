from flask import Blueprint,jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from app.helper import validate_model
import datetime
from app.slack_message import post_slack_message

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)
        
        db.session.add(new_task)
        db.session.commit()

        return make_response(jsonify({"task": new_task.to_dict()}), 201)
        

    except KeyError as error:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
        
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = Task.query

    sort_query = request.args.get("sort")
    if sort_query == "asc":
        task_query = task_query.order_by(Task.title.asc())
    else:
        task_query = task_query.order_by(Task.title.desc())

    tasks = task_query.all()
    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return jsonify({"task":task.to_dict()})

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task.to_dict()})

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})
    
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.date.today().isoformat()

    db.session.commit()
    post_slack_message(task)

    return jsonify({"task":task.to_dict()})

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return jsonify({"task":task.to_dict()})
    
    