from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#VALIDATE TASKS
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"book {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":"There's no {task_id} sorry."}))
    return task


#POST endpoint CREATES A NEW TASK
@tasks_bp.route("", methods=["POST"])
def create_task():
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        is_complete=request_body["Completed?"])

        
        db.session.add(new_task)
        db.session.commit()

        return make_response(f"Made a new task: {new_task.title}", 201)

#GET THE TASKS
@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    task_force = [task.to_dict for task in tasks]
        # task_force.append({
        #     "id": task.id,
        #     "title": task.title,
        #     "description": task.description,
        #     "completed at":task.completed_at
        # })
    return make_response(jsonify(task_force), 200)

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_tasks(task_id):
    task = validate_task(task_id)
    
    return task.to_dict(), 200

#Update a task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(f"The task {task.id} was updated!!")

#DELETES A TASK
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"The task {task.title} was deleted!")