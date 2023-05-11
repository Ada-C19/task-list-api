from flask import Blueprint,jsonify, abort,make_response,request
from app import db
from app.models.task import Task
from datetime import datetime

task_list_bp = Blueprint("tasks", __name__, url_prefix ="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix = "/goals")

@task_list_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()
    print(request_body)
    print("************")
    
    if (not "title" in request_body) or (not "description" in request_body):
        return{
            "details":"Invalid data"
        }, 400
    try:
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()

        #message = f"Task {new_task.title} successfully created"
        return make_response(jsonify({"task":new_task.task_dict()}), 201)
    
    except KeyError as e:
        abort(make_response("Invalid request. Missing required value: {e}"), 400)

@task_list_bp.route("/<id>", methods = ["GET"])
def get_one_saved_task(id):
    task = validate_task(id)
    return jsonify({"task":task.task_dict()}), 200
 
@task_list_bp.route("", methods = ["GET"])
def get_all_saved_tasks():
    sort_query=request.args.get("sort")
    tasks_query=Task.query
    
    if sort_query =="asc":
        tasks_query = Task.query.order_by(Task.title.asc())
    elif sort_query =="desc":
        tasks_query = Task.query.order_by(Task.title.desc())
    
    tasks = tasks_query.all()

    tasks_response =[task.task_dict() for task in tasks]

    return (jsonify(tasks_response)),200
        
    
    
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    
    task = Task.query.get(task_id)
  
    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task


@task_list_bp.route("/<id>", methods = ["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    response_body = {"task":task.task_dict()}
    
    
    return make_response(jsonify(response_body), 200)

@task_list_bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task= validate_task(id)

    db.session.delete(task)
    db.session.commit()

    message = {"details":f'Task {task.task_id} "{task.title}" successfully deleted'}
    return make_response(jsonify(message), 200)


@task_list_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task=validate_task(id)
    task.completed_at=datetime.now()
    db.session.commit()

    return jsonify({"task":task.task_dict()}), 200



@task_list_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task=validate_task(id)
    task.completed_at=None
    db.session.commit()

    return jsonify({"task":task.task_dict()}), 200
    

        
    
    
    
    
    