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

#create one task -POST /tasks/<id> - (CREATE)
@tasks_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()
        # if "title" not in request_body or "decription" not in request_body or "completed_at" not in request_body:
        #     return make_response("Invalid Request",400)
        
    new_task = Task.create_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":new_task.to_dict()}), 201





