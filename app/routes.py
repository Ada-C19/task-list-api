from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#Wave 1- CRUD
#CREATES NEW TASK ENDPOINT
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()


    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit() 

    return make_response(jsonify({"task": new_task.to_dict()}), 201) 


#GET ALL TASK ENDPOINTS
@tasks_bp.route("", methods=["GET"])
def read_all_tasks(): 

    tasks = Task.query.all()

    #Wave 2- Query Params-----
    sort_query_param = request.args.get("sort")

    if sort_query_param == "asc":
        tasks = Task.query.order_by(task.title)

    elif sort_query_param == "desc":
        tasks = Task.query.order_by(task.title) 
    
    #-----------

    response_body = []

    for task in tasks:
       response_body.append(task.to_dict())

    return jsonify(response_body)

#GET ONE TASK ENDPOINT  
@tasks_bp.route("/<task_id>", methods=["GET"])

def handle_task(task_id):
    task = validate_task(task_id)

    return make_response({"task": task.to_dict()}) 
                         



#UPDATE ONE ENDPOINT
@tasks_bp.route("/<task_id>", methods = ["PUT"])

def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200) 

#DELETE ONE ENDPOINT
@tasks_bp.route("/<task_id>", methods = ["DELETE"])

def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}), 200)



#HELPER FUNCTION
def validate_task(task_id):
    try: 
        task_id = int(task_id)
    except: 
        abort(make_response({"message": f"Task {task_id} is invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} was not found."}, 404))
    
    return task 


#WAVE 3 - Patch
# @tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
# def mark_complete(task_id):
#     task = validate_task(task_id)

#     task.completed_at = #date/time

#     db.session.patch(task)
#     db.session.commit()

#     return make_response()

#WAVE 4- Slack API 