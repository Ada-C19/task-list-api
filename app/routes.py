from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({'msg': f"invalid id {task_id}"}, 400))
    
    task = Task.query.get(task_id)
    
    return task if task else abort(make_response({'msg': f"No task with id {task_id}"}, 404))


@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201




