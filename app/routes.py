from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task

goal_bp = Blueprint("goal", __name__, url_prefix="/goal")
task_bp = Blueprint("task", __name__, url_prefix="/task")

@task_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    
    task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
                }
                    }), 201

@task_bp.route("", methods = ["GET"])
def read_all_tasks():
    title_query = request.args.get("title")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()
        
    tasks_response = []
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response)