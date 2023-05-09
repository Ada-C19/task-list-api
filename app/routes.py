from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app.models.goal import Goal

task_list_bp = Blueprint("task_list", __name__)

def validate_model_task(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    task = cls.query.get(model_id)
    goal = cls.query.get(model_id)

    if not task:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return task


def validate_model_goal(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    goal = cls.query.get(model_id)

    if not goal:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return goal