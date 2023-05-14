from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort


task_list_bp = Blueprint("task_list", __name__, url_prefix="/tasks")




# create
@task_list_bp.route("", methods=["POST"])

def post_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
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
        if not tasks:
            return jasonify(task_response)

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


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))
    task = Task.query.get(task_id)
    
    if not task:
        abort(make_response({"details": "Invalid Data"}, 404))
    return task
    
#read one task/ read if empty task. 

@task_list_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    if not task.completed_at:
        return {"task":
        {"id":task.task_id,
        "title":task.title,
        "description": task.description,
        "is_complete": False

        }}
    else:
        return {"task":{
        "id":task.task_id,
        "title":task.title,
        "description": task.description,
        "completed_at":task.completed_at
        }}


# #update
@task_list_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(f"Task {task.task_id} succsefully updated", 200)


# # delete
@task_list_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return abort(make_response({"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}))
