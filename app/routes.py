from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


#CREATES NEW TASK ENDPOINT
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()


    #new_task = Task.from_dict(request_body)
    new_task = Task(
        title = request_body["title"], 
        description = request_body ["description"])
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task: {new_task.title} successfully created", 201)


#GET ALL TASK ENDPOINTS
@tasks_bp.route("", methods=["GET"])
def read_all_tasks(): 

    #Wave 2- Query Params 
    sort_query_param = request.args.get("sort")

    if sort_query_param == "asc":
        tasks = Task.query.order_by(task.title)

    else:
        sort_query_param == "desc"
        tasks = Task.query.order_by(task.title)

    response_body = []

    for task in tasks:
       response_body.append(task.to_dict())

    return jsonify(response_body)

#GET ONE TASK ENDPOINT  
@tasks_bp.route("/<task_id>", methods=["GET"])

def handle_task(task_id):
    task = validate_task(task_id)

    return make_response(task.to_dict())


#UPDATE ONE ENDPOINT
@tasks_bp.route("/<task_id>", methods = ["PUT"])

def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return make_response(f"Task: {task.title} successfully updated", 201)


#DELETE ONE ENDPOINT
@tasks_bp.route("/<task_id>", methods = ["DELETE"])

def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task {task.title} successfully deleted", 200)


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