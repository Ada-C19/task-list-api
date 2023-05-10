from flask import Blueprint,make_response,request,jsonify,abort
from app import db
from app.models.task import Task
from app.helper import validate_task

#CREATE BP/ENDPOINT
tasks_bp = Blueprint("tasks",__name__, url_prefix="/tasks")

#GET ALL tasks [GET]/tasks :(CREATE)
@tasks_bp.route("",methods=["GET"])
def get_all_tasks():
    if request.args.get("sort") == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif request.args.get("sort") == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response),200


#GET one task [GET]/tasks/<id> :(CREATE)
@tasks_bp.route("/<id>",methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return jsonify({'task':task.to_dict()}),200

#CREATE one task/must contain title+description [POST]/tasks/<id> :(CREATE)
@tasks_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()

    try:
        if request_body["title"] or request_body["description"]:
            new_task = Task.create_dict(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201

#UPDATE one task/RETURN msg not found [PUT]/tasks/<id> :(UPDATE)
@tasks_bp.route("/<id>",methods=["PUT"])
def update_task(id):
    task = Task.query.get(id) #SQLA used to retrieve row from db tbl to update/delete
    if task is None:
        return jsonify({'error': 'Task not found'}),404
    
    request_body = request.get_json()
    task.update_dict(request_body)
    db.session.commit()

    return jsonify({'task':task.to_dict()}),200


#DELETE one task [DELETE]/tasks/<id> :(DELETE)
@tasks_bp.route("/<id>",methods=["DELETE"])
def delete_task(id):
    task_to_delete = validate_task(id)

    db.session.delete(task_to_delete)
    db.session.commit()

    message = {'details': f'Task {id} "{task_to_delete.title}" successfully deleted'}

    return make_response(message,200)













