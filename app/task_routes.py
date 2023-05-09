from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app import db
from datetime import datetime

tasks_bp = Blueprint("tasks_db", __name__, url_prefix="/tasks")

# Create
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    check_task_data(request_body)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)


# Read
@tasks_bp.route("", methods=["GET"])
def list_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.order_by(Task.title.asc()).all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response)




def check_task_data(request):
    if "title" not in request or "description" not in request:
        return abort(make_response({"details": "Invalid data"}, 400))
