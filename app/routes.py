from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task

goal_bp = Blueprint("goal", __name__, url_prefix="/goal")
task_bp = Blueprint("task", __name__, url_prefix="/task")

#TASK ROUTES

@task_bp.route("", methods=['POST'])

def create_task():

    request_body = request.get_json()

    
    task = Task(title=request_body["title"],
                description=request_body["description"],
                completed_at=request_body["completed_at"])

    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
                }
                    }), 201

@task_bp.route("", methods = ["GET"])
def read_all_tasks():

    title_query = request.args.get("title")
    description_query = request.args.get("description")
    is_complete_query = request.args.get("is_complete")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif description_query:
        tasks = Task.query.filter_by(description=description_query)
    elif completed_query:
        tasks = Task.query.filter_by(description=is_complete_query)
    else:
        tasks = Task.query.all()
        
    tasks_response = []
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods = ["GET"])
def read_one_task(task_id):
    
    task = validate_model(Task, task_id)

    return jsonify({"task":task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = validate_model(Task, task_id)
    
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})






def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type ({type(model_id)}). Must be an integer)"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} does not exist"}, 404))
        
    return model

