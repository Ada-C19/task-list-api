from flask import Blueprint, request, make_response, jsonify, abort
from .models.task import Task
from app import db

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

# Read all tasks:
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("sort") 

    if title_query == "asc":
        task_objects = Task.query.order_by(Task.title) 
        # task_objects = Task.query.order_by(Task.title).all()
    elif title_query == "desc":
        task_objects = Task.query.order_by(Task.title.desc()) 
    else:
        task_objects = Task.query.all()
    task_list = [Task.to_dict(task) for task in task_objects]
    return make_response(jsonify(task_list), 200)
 
 # Read one task:
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task_object_list = validate_model(Task, task_id)#Task.query.filter_by(task_id=task_id).all()
    # task_list = [Task.to_dict(task) for task in task_object]
    # return make_response(jsonify(task_list), 200)
    response = Task.add_task_key(Task.to_dict(task_object_list))
    return make_response(response, 200)

# Create task:
@task_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body_dict = request.get_json()
        task_object = Task.from_dict(request_body_dict)
        db.session.add(task_object)
        db.session.commit()
        response_object_list = Task.query.all()
        # response_body ={"task":{"id":response_object[0].task_id,
        #                         "title":request_body_dict["title"],
        #                         "description":request_body_dict["description"],
        #                         "is_complete": False}} #request_body["completed_at"]
        response_dict = Task.to_dict(response_object_list[0])
        return make_response(Task.add_task_key(response_dict), 201)
    except(KeyError):
        return make_response({"details": "Invalid data"}, 400)
    
# Update a task
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task_object = validate_model(Task, task_id)
    task_request_body_dict = request.get_json()

    if task_request_body_dict.get("title"):
        task_object.title = task_request_body_dict.get("title")
    if task_request_body_dict.get("description"):
        task_object.description = task_request_body_dict.get("description")
    if task_request_body_dict.get("completed_at"):
        task_object.complete_at = task_request_body_dict.get("completed_at")
    db.session.commit()
    return Task.add_task_key(Task.to_dict(task_object))

# Delete a task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    response_object = validate_model(Task, task_id)
    db.session.delete(response_object)
    db.session.commit()
    return make_response({
        'details': f'Task {response_object.task_id} "{response_object.title}" successfully deleted'}, 200)


def validate_model(cls, task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details" : f"It is not a valid id {task_id}"}, 400))
    response = cls.query.get(task_id)
    if not response:
        abort(make_response({"details" : f"{cls.__name__} #{task_id} not found"}, 404))
    return response





