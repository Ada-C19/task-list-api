from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort

task_list_bp = Blueprint("task_list_bp", __name__, url_prefix="/tasks")

def validate_model_task(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    task = cls.query.get(model_id)

    if not task:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return task


# def validate_model_goal(cls, model_id):
#     try:
#         model_id = int(model_id)
#     except:
#         abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

#     goal = cls.query.get(model_id)

#     if not goal:
#         abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

#     return goal

@task_list_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.task_from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)

@task_list_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.task_to_dict())
    
    return jsonify(tasks_response)


# @task_list_bp.route("", methods=["GET"])
# def say_hi_new_task():
#     my_response = "Please create a new task"
#     return my_response