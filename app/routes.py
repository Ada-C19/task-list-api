from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request


task_list_bp = Blueprint("task_list", __name__, url_prefix="/tasks")




# create
@task_list_bp.route("", methods=["POST"])

def post_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid request", 400)
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit() 
    
    return make_response(f"New task: {new_task.title},  created", 201)

# #read
@task_list_bp.route("", methods=["GET"])

def get_all_tasks():
    
    task_response = []
    tasks = Task.query.all()
    
    for task in tasks:
        if not task.completed_at:
            task_response.append({"id":task.task_id,
            "title":task.title,
            "description": task.description,
            "is_complete": False

            })
        else:
            task_response.append({
            "id":task.task_id,
            "title":task.title,
            "description": task.description,
            "completed_at":task.completed_at
        })
    return jsonify(task_response)


# #update

# # delete


