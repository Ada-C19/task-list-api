from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from datetime import datetime 
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
    task = validate_task(task_id)

    return make_response({"task": task.to_dict()}) 
                         



#UPDATE ONE ENDPOINT
@tasks_bp.route("/<task_id>", methods = ["PUT"])

def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200) 

#DELETE ONE ENDPOINT
@tasks_bp.route("/<task_id>", methods = ["DELETE"])

def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}), 200)



#HELPER FUNCTION
def validate_task(task_id):
    try: 
        task_id = int(task_id)
    except: 
        abort(make_response({"message": f"Task {task_id} is invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} was not found."}, 404))
    
    return task 


#WAVE 3 - PATCH

@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    
    task = validate_task(task_id)

    if task.completed_at is None:
        task.completed_at = datetime.now()
        
        db.session.patch(task)
        db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)

@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):

    task = validate_task(task_id)

    if task.completed_at is not None:
        task.completed_at = None

        db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)



#xoxb-4680452269380-5265102669844-cwaf1y2RJchsv5Az9NdAJt9r

#------------------------------------------------------------------------------------

@goals_bp.route("", methods=["POST"])

def create_goal():
    request_data = request.get_json()
    goal = Goal.from_dict(request_data)

    db.session.add(goal)
    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return make_response(jsonify(response_body), 201)

@goals_bp.route("", methods=["GET"])

def get_goals():

    goals = Goal.query.all()

    for goal in goals:
       response_body.append(goal.to_dict())

    return make_response(jsonify(response_body), 200)

@goals_bp.route("/<goal_id>", methods=["GET"])

def get_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"Task {goal_id} was not found."}, 404))

    response_body = {"goal": goal.to_dict()}

    return make_response(jsonify(response_body), 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])

def update_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        abort(make_response({"message": f"Task {goal_id} was not found."}, 404))

    request_data = request.get_json()
    goal.title = request_data["title"]

    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return make_response(jsonify(response_body), 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])

def delete_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        abort(make_response({"message": f"Task {goal_id} was not found."}, 404))

    db.session.delete(goal)
    db.session.commit()

    response_body = {
        "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    }

    return make_response(jsonify(response_body), 200)