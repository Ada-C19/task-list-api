from flask import Blueprint,make_response,request,jsonify,abort
from app import db
from app.models.task import Task
from app.helper import validate_task

#CREATE BP/ENDPOINT
tasks_bp = Blueprint("tasks",__name__, url_prefix="/tasks")

# GET all Tasks - /tasks - (CREATE)
@tasks_bp.route("",methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_query = request.args.get("is_completed")
    
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif description_query:
        tasks = Task.query.filter_by(description=description_query)
    elif completed_query: 
        tasks = Task.query.filter_by(is_completed = completed_query)
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response),200


# GET one Tasks - /tasks/<id> - (CREATE)
@tasks_bp.route("/<id>",methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return jsonify({'task':task.to_dict()}),200

#CREATE one task -POST /tasks/<id> - (CREATE)
@tasks_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()
        
    new_task = Task.create_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":new_task.to_dict()}), 201

#UPDATE a task/ RETURN msg not found -PUT / tasks/<id> - (UPDATE)
@tasks_bp.route("/<id>",methods=["PUT"])
def update_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({'error': 'Task not found'}),404
    
    request_body = request.get_json()
    task.update_dict(request_body)
    db.session.commit()

    return jsonify({'task':task.to_dict()}),200


#DELETE one task -DELETE /tasks/<id> - (DELETE)
@tasks_bp.route("/<id>",methods=["DELETE"])
def delete_task(id):
    task_to_delete = validate_task(id)

    db.session.delete(task_to_delete)
    db.session.commit()

    message = {'details': f'Task 1 "{task_to_delete.title}" successfully deleted'}

    return make_response(message,200)

#CREATE task must contain title/description - POST /tasks/<id> - (CREATE)
# @tasks_bp.route("",methods=["POST"])
# def create_task_must_contain_title():
#     request_body = request.get_json()
#     if not request_body or "title" not in request_body:
#         return make_response({"details": "Invalid data, request must contain title."}, 400)    
#     elif "description" not in request_body:
#         return make_response({"details":"Invalid data, ruest must contain description"},400)
        
#     new_task = Task.create_dict(request_body)

#     db.session.add(new_task)
#     db.session.commit()

#     return make_response({"task":new_task.to_dict()}), 201
    





