from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

task_list_bp = Blueprint("task_list_bp", __name__, url_prefix="/tasks")

### Get Tasks: No Saved Tasks
### Get Tasks: Getting Saved Tasks
@task_list_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    tasks_response = []
    if len(tasks) != 0:
        for task in tasks:
            tasks_response.append( {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
                } )
        
    return jsonify(tasks_response)

### Create a Task: Valid Task With `null` `completed_at`
@task_list_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
    db.session.add(new_task)
    db.session.commit()
    
    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False    
    } }, 201
            
### Get One Task: One Saved Task
@task_list_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(Task, task_id)
    
    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
    } }

### Update Task
@task_list_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(Task, task_id)
    
    request_data = request.get_json()
    
    task.title = request_data["title"]
    task.description = request_data["description"]
    
    db.session.commit()
    
    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False    
    } }

### Delete Task: Deleting a Task
@task_list_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}

    
### No matching Task: Get, Update, and Delete


### Create a Task: Invalid Task With Missing Data

#### Missing `title`

#### Missing `description`

#### Missing `completed_at`

# Helper function
def validate_task (model, item_id):
    try:
        item_id_int = int(item_id)
    except:
        return abort(make_response({"message":f"task {item_id_int} invalid"}, 400))
    
    return model.query.get_or_404(item_id)