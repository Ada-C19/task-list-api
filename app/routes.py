from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc, asc
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# Route to get tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    query_sort = request.args.get("sort")
    
    if query_sort == "asc":
        tasks = db.session.query(Task).order_by(asc(Task.title)).all()
    elif query_sort == "desc":
        tasks = db.session.query(Task).order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response), 200


# Validate ID function
def validate_model(cls, model_id):
    model_item = cls.query.get(model_id)

    if not model_item:
        return abort(make_response({"message": f"{cls.__name__} with ID {model_id} not found."}, 404))

    return model_item

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):

    task = validate_model(Task, task_id)

    return {"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}, 200

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try: 
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"]
        )  
    except:
        return {
            "details": "Invalid data"
        }, 400
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }}), 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"],
    task.description = request_body["description"]
    
    db.session.commit()

    return jsonify({"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
    }, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.utcnow()

    db.session.commit()
    
    return {"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
        }}, 200


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(
            title = request_body["title"]
        )
    except:
        return {
            "details": "Invalid data"
        }, 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": {
            "id": new_goal.id,
            "title": new_goal.title
        }
    }), 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.id,
            "title": goal.title
            })
    
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {
        "goal": {
            "id": goal.id,
            "title": goal.title
        }
    }, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    
    goal.title = request_body["title"],
    
    db.session.commit()

    return jsonify({"goal": {
            "id": goal.id,
            "title": goal.title
            }}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({
        "details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"
        }), 200