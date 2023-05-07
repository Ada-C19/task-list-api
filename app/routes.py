from flask import Blueprint, request, make_response, request, abort, jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    if len(request_body) != 3:
        return make_response({"details": "Invalid data"}, 400)
    #
    # if not request_body["title"]:
    #     return make_response({"details": "Invalid data"}, 400)
    new_task = Task(
            title= request_body["title"],
            description= request_body['description'],
            completed_at= request_body['completed_at']
        )
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.from_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    total_tasks = Task.query.all()
    
    for task in total_tasks:
        # tasks_response.append({
        #     "id": task.task_id,
        #     "title": task.title,
        #     "description": task.description,
        #     "is_complete": False
        # })
        tasks_response.append(task.from_dict())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=['GET'])
def read_one_task(task_id):
    # task = Task.query.get(task_id)
    task = validate_item(task_id)

    is_complete = False
    if not task.completed_at:
        is_complete = False

    return {"task":{
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        # "is_complete": False
        "is_complete": is_complete
    }
    }, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    # task = Task.query.get(task_id)
    task = validate_item(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]


    db.session.commit()

    is_complete = False
    if not task.completed_at:
        is_complete = False

    return {"task":{
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        "is_complete": False,
        "is_complete": is_complete
    }
    }, 200

######GET CLARIFICATION ON THE RETURN MESSAGE
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    # task = Task.query.get(task_id)
    task = validate_item(task_id)

    db.session.delete(task)
    db.session.commit()

# return {
#   "details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
# },
#make response returnse a status code 200
# return make_response({
#     "details": "Task {task.task_id}"
# })

    return make_response(f"Task {task.task_id} successfully deleted")
    

def validate_item(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"invalid task_id: {task_id}"}, 400))
    
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task