from flask import Blueprint,jsonify, abort, make_response,request
from app import db
from app.models.task import Task

tasks_bp = Blueprint ("tasks", __name__, url_prefix="/tasks")

def handle_id_request(cls,id):
    try:
        id = int(id)
    except:
        abort(make_response(jsonify({"message":f"{cls.__name__} {id} invalid"}),400))

    Object = cls.query.get(id)

    if not Object:
        abort(make_response({"message":f"{cls.__name__} {id} not found"},404))
        

    return Object


@tasks_bp.route("", methods=["POST"])

def create_task():

    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"},400)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    task_response = new_task.to_dict()

    return make_response(jsonify ({"task":task_response}), 201)


@tasks_bp.route("", methods=[ "GET"])

def read_all_tasks():

    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        print("ASCENDED")
        tasks=Task.query.order_by(Task.title.asc())
    elif sorting_query=="desc":
        print("DESCENDED")
        tasks=Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks: 
        tasks_response.append(task.to_dict())
    
    return make_response(jsonify (tasks_response), 200)

@tasks_bp.route("/<task_id>", methods=["GET"])

def read_one_task(task_id):
    task=handle_id_request(Task, task_id)
    #task = Task.query.get(task_id)

    task_response = task.to_dict()
    return make_response({"task": task_response},200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    
    updated_task=handle_id_request(Task, task_id)
    request_body = request.get_json()

    updated_task.title = request_body["title"]
    updated_task.description = request_body["description"]

    db.session.commit()

    task_response = updated_task.to_dict()

    return make_response(jsonify ({"task":task_response}), 200)

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task= handle_id_request(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f'Task {task.task_id} "{task.title}" successfully deleted'},200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PUT"])
def finished_task(task_id):
    
    updated_task=handle_id_request(Task, task_id)

    #updated_task.completed_at = (2012, 9, 1)
    updated_task.title= "WASHUUU"

    

    db.session.commit()

    task_response = updated_task.to_dict()
    print (task_response)

    return make_response(jsonify ({"task":task_response}), 200)