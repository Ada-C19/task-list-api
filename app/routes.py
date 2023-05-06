from flask import Blueprint, request, make_response, request, abort, jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
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
