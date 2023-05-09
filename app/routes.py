from app import db
from .models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    response = {"task": new_task.to_dict()}

    return make_response(jsonify(response), 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_param = request.args.get("title")
    
    if title_param:
        tasks = Task.query.filter_by(title=title_param)
    else:
        tasks = Task.query.all()

    task_list=[task.to_dict()for task in tasks]

    return jsonify(task_list), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_planet(task_id):

    task = validate_model(Task, task_id)
    response = {"task": task.to_dict()}

    return make_response(jsonify(response), 200)













# HELPER FUNCTION
def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} was invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} with id {id} was not found"}, 404))
    
    return model