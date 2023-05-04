from flask import Blueprint

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# get all endpoint
@bp.route("", methods=["GET"])
def get_all_tasks():
    pass
