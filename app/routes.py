from flask import Blueprint, jsonify, abort, make_response, request
from .models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# create task route POST
# update task route UPDATE
# delete task route DELETE