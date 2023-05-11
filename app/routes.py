from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
# from app.models.task import Goal
from datetime import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# definbe a route for creating a task resource

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message:" f"{model_id} The id is invalid"}, 400))
    model = cls.query.get(model_id)
    if not model:
        abort(make_response("message:" f"{cls.__name__} {model_id} The id is invalid", 404))
    return model

def validate_model_by_key(cls, model_title):
    try:
        model_tilte = int(model_title)
    except:
        abort(make_response({"details:" f"Invalid data"}, 400))
    model = cls.query.get(model_title)
    
    return model


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not request_body.get("title"):
        return jsonify({"details": "Invalid data"}), 400
    elif not request_body.get("description"):
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.to_dict()}, 201

@task_bp.route("", methods=["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort", "asc")
    title_query = request.args.get("title")
    description_query = request.args.get("description")
   

    if sort_query == "asc":
        # tasks = Task.query.order_by(sort = sort_query)
        tasks = Task.query.order_by(Task.title.asc())

    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())

    elif title_query:
        tasks = Task.query.filter_by(title = title_query)

    elif description_query:
        tasks = Task.query.filter_by(description = description_query)

    else:
        tasks = Task.query.all()

    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def read_single_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict_one_task(), 200    


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title  = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at  = request_body["completed_at"]
    # task.is_complete = request_body["is_complete"]

    db.session.commit()

    # return jsonify({"task":task.to_dict()}, 200)
    return task.to_dict_one_task(), 200
    # return jsonify((f"Yayy! task {task.to_dict()} is succesfully updated!"), 200)
    # return (task.to_dict(),f"Yayy! task {task_id} is succesfully updated!"),200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    # return jsonify(f"Task {task_id} is succesfully deleted!")

    return jsonify({"details":f'Task {task_id} "{task.title}" successfully deleted'}), 200

    # return jsonify(f"{"details":task_id} successfully deleted"),200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    if task is None:
        abort(make_response({"message:" f"{task_id} Task not found"}, 404))
    elif task.completed_at is None:
        task.completed_at = datetime.utcnow()
        task.is_complete = True

        db.session.commit()
        return jsonify({"task": task.to_dict()}), 200
    else:
        task.is_complete = True

        db.session.commit()
        return jsonify({"task": task.to_dict()}), 200
    
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task is None:
        abort(make_response({"message:" f"{task_id} Task not found"}, 404))
    elif task.completed_at is None:
        task.is_complete = False

        db.session.commit()
        return jsonify({"task": task.to_dict()}), 200
    else:
        task.completed_at = None
        task.is_complete = False

        db.session.commit()
        return jsonify({"task": task.to_dict()}), 200
    
    
    
    







    






