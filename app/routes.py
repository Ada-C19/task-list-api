from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import date

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#TASK ROUTES

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type ({type(model_id)}). Must be an integer)"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} does not exist"}, 404))
        
    return model

###

@tasks_bp.route("", methods=['POST'])

def create_task():

    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "is_complete" == False:
        abort(make_response({"details": "Invalid data"}, 400))
    
    new_task = Task(title=request_body["title"],
                description=request_body["description"])
        
    if "completed_at" in request_body:
        new_task.completed_at=request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task": new_task.to_dict()
    }, 201

@tasks_bp.route("", methods = ["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
        
    tasks_response = []
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods = ["GET"])
def read_one_task(task_id):
    
    task = validate_model(Task, task_id)

    return jsonify({"task":task.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = validate_model(Task, task_id)
    
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.add(task)
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})



@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):

    task = validate_model(Task, task_id)
        
    task.completed_at = date.today()

    db.session.add(task)
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):

    task = validate_model(Task, task_id)
        
    task.completed_at = None

    db.session.add(task)
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

#################################GOAL ROUTES #############################################

@goals_bp.route("", methods=['POST'])

def create_goal():

    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    
    return {
        "goal": new_goal.to_dict()
    }, 201

    


@goals_bp.route("", methods = ["GET"])

def read_all_goals():
    goals = Goal.query.all()
        
    goals_response = []
    
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return jsonify(goals_response), 200



@goals_bp.route("/<goal_id>", methods = ["GET"])
def read_one_goal(goal_id):
    
    goal = validate_model(Goal, goal_id)

    return jsonify({"goal":goal.to_dict()}), 200



@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    task = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    
    goal.title = request_body["title"]

    db.session.add(goal)
    db.session.commit()

    return jsonify({"goal":goal.to_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"})


