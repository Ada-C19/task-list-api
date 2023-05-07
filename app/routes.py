from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort 

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#validates task
def validate_model_by_id(model, id):
    #handle invalid task id, return 400
    try:
        id = int(id)
    except: 
        abort(make_response(jsonify({"msg": f"{model.__name__}{id} is invalid."}), 400))
    
    model_object = model.query.get(id)
    
    if model_object is None:
        abort(make_response(jsonify({"msg": "task not found"}), 404))

    return model_object 

#creates one task
@tasks_bp.route ("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")
    if not description or not title:
        return {"details": "Invalid data"}, 400
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at is not None}
    }, 201

#reads one task as long as at least one is saved   
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("title")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    #grab all info from the instance task table
    else:
        tasks = Task.query.all()
        
    task_dict = [task.to_dict() for task in tasks]
    return jsonify(task_dict), 200

#gets one task by id
@tasks_bp.route("/<task_id>", methods=["GET"])
def single_task(task_id):
    task = validate_model_by_id(Task, task_id)
    return jsonify({"task": task.to_dict()}), 200

#update task by id 
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    get_task = Task.query.get(task_id)
    task = validate_model_by_id(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]


    db.session.commit()
    
    return jsonify({"task": task.to_dict()}), 200

#deletes single task by id
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_single_task(task_id):
    task = validate_model_by_id(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    success_message = f"Task {task.task_id} \"{task.title}\" successfully deleted"
    return jsonify({"details": success_message}), 200

