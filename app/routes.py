from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__,url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()

        return make_response({
            "task":{
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": False
            }}, 201)
    
    except KeyError as e:
        abort(make_response({"message":f"Missing required value: {e}"}, 400))

# def validate_model(cls, model):
#     try:
#         model_id = int(model_id)
#     except:
        

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    task_list = [task.to_dict() for task in tasks]

    # for task in tasks:
    #     task_list.append(task.to_dict())
    
    return make_response(jsonify(task_list), 200)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task():
    pass