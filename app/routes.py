from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#VALIDATE TASKS
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"There's no {model_id} sorry."}, 404))
    return model


#POST endpoint CREATES A NEW TASK
@tasks_bp.route("", methods=["POST"])
def create_task():
        request_body = request.get_json()
        try:
            new_task = Task.from_dict(request_body)
        except KeyError:
            return {
                "details": "Invalid data"
            }, 400
        db.session.add(new_task)
        db.session.commit()

        return {f"task": new_task.to_dict()}, 201

#GET THE TASKS
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort = request.args.get("sort")

    if sort == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
        
    task_force = [task.to_dict() for task in tasks]
    return jsonify(task_force), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_tasks(task_id):
    task = validate_model(Task, task_id)
    
    return {f"task":task.to_dict()}, 200

#Update a task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}

#DELETES A TASK
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({'details': f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)