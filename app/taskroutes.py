from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from datetime import datetime 
from .routes import validate_model
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#WAVE 1- CRUD
#CREATES NEW TASK ENDPOINT
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit() 

    return make_response(jsonify({"task": new_task.to_dict()}), 201)  


#GET ALL TASK ENDPOINTS -- WAVE 2 QUERY PARAM
@tasks_bp.route("", methods=["GET"])

def read_all_tasks():
    sort_query_param = request.args.get("sort")
    
    if sort_query_param == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query_param == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    response_body = []
    
    for task in tasks:
        response_body.append(task.to_dict())

    return jsonify(response_body)

#GET ONE TASK ENDPOINT  
@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_model(Task, task_id)
    
    response_body = {
        "task": {
            "id": task.id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
    }
    
    return make_response(jsonify(response_body), 200)
                         



#UPDATE ONE ENDPOINT
@tasks_bp.route("/<task_id>", methods = ["PUT"])

def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200) 

#DELETE ONE ENDPOINT
@tasks_bp.route("/<task_id>", methods = ["DELETE"])

def delete_task(task_id):

    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task.id} \"{task.title}\" successfully deleted"}), 200)





#WAVE 3 - PATCH

@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):

    task = validate_model(Task, task_id)


    if task.completed_at is None:
        task.completed_at = datetime.now()
        
    #    db.session.patch(task)
        db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)


@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):

    task = validate_model(Task, task_id)

    if task.completed_at is not None:
        task.completed_at = None

        db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)




#xoxb-4680452269380-5265102669844-cwaf1y2RJchsv5Az9NdAJt9r

#------------------------------------------------------------------------------------
