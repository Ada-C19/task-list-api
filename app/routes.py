from flask import Blueprint, make_response, request, jsonify, abort
from app.models.task import Task
from app import db


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def make_tast():
    try:
        request_body = request.get_json()

        new_task = Task(
            title = request_body["title"],
            description =  request_body["description"],
            completed_at = request_body["completed_at"]
        )

        db.session.add(new_task)
        db.session.commit()

        return make_response({
"task": {
    "id": new_task.task_id,
    "title": new_task.title,
    "description": new_task.description,
    "is_complete": bool(new_task.completed_at)
}
}, 201)
    except KeyError as error:
        abort(make_response(f"{error.__str__()} is missing", 400))