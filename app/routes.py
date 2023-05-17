from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#TASK ROUTES

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type ({type(model_id)}). Must be an integer)"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} does not exist"}, 404))
        
    return model

###

@tasks_bp.route("", methods=['POST'])

def create_task():

    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "is_complete" == False:
        abort(make_response({"details": "Invalid data"}, 400))
    
    new_task = Task(title=request_body["title"],
                description=request_body["description"])
        
    if "completed_at" in request_body:
        new_task.completed_at=request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task": new_task.to_dict()
    }, 201

@tasks_bp.route("", methods = ["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
        
    tasks_response = []
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods = ["GET"])
def read_one_task(task_id):
    
    task = validate_model(Task, task_id)

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = validate_model(Task, task_id)
    
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.add(task)
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})








