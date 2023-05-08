from flask import Blueprint,jsonify, request, make_response, abort
from app.models.task import Task
from app import db


task_bp = Blueprint("tasks", __name__,url_prefix="/tasks")

#post a task
@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)


    db.session.add(new_task)
    db.session.commit()

    return {"task" : new_task.to_dict()}, 201


@task_bp.route("", methods=["GET"])
def get_tasks():
    response = []
    title_query = request.args.get("title")

    if title_query is None:
        all_tasks = Task.query.all()
    else:
        all_tasks = Task.query.filter_by(title=title_query)

    for task in all_tasks:
        response.append(task.to_dict())

    return jsonify(response), 200

@task_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    validate_id(Task,id)

    task = Task.query.get(id)

    return {"task" : task.to_dict()}, 200


def validate_id(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid endpoint: {item_id}"},404))
    
    return model.query.get_or_404(item_id)



