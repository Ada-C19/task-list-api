from flask import Blueprint, db, jsonify, request


task_bp = Blueprint("tasks"), __name__,url_prefix="/tasks"

#post a task
@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    # new_task = 

    db.session.add(new_task)
    db.session.commit()

    return {"id": new_task.id}, 201
