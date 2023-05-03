from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    return jsonify([]), 200