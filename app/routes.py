from flask import Blueprint, make_response, jsonify, request, abort
from app.models.task import Task
from app import db

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# def validate_request_body(request): finish later 



@bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_list = []
    for task in tasks:
        tasks_list.append(task.to_dict()) 
        # tasks_list.append(task)
        
        # tasks_list.append(f"{
        #   "id:" {task.id}","
        #   "title:" {task.title}","
        #    "description:" {task.description}",
        #      "completed_at:" {task.completed_at}
        #    }")
        # tasks_list.append({
        #     "id": task.id,
        #     "title": task.title,
        #     "description": task.description,
        #     "completed_at": task.completed_at
        # })
    
    return jsonify(tasks_list), 200


@bp.route("", methods=["POST"])
def create_task():
    request_body=request.get_json()
    
    if "title" not in request_body or not request_body["title"] or "description" not in request_body or not request_body["description"]:
        abort(make_response({"details": "Invalid data"}, 400))
    else:

        is_complete = request_body.get("is_complete", False) #find a way to include this in model class


        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            is_complete=is_complete
        )

        # new_task = Task.from_dict(request_body)
        
        db.session.add(new_task)
        db.session.commit()
        
        return {"task": new_task.to_dict()}, 201



def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response(f"Task number {id} not valid", 400))
    
    task = Task.query.get(id)

    if not task:
        abort(make_response(f"Task number {id} was not found", 404))
    
    return task



@bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)
    return {"task": task.to_dict()}, 200


@bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json()
    is_complete = request_body.get("is_complete", False)

    # is_complete = request_body.get("is_complete", False)

    # if request_body["is_complete"] == None:
    #     request_body["is_complete"] = False

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.is_complete = is_complete 

    db.session.commit()

    return {"task": task.to_dict()}, 200

@bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    return {"details" : f'Task {id} "{task.title}" successfully deleted'}, 200




