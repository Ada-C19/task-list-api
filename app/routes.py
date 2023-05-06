from flask import Blueprint, jsonify, request, Response
from app.models.task import Task
from app import db 


# create blueprint 
task_bp = Blueprint("task", __name__, url_prefix="/tasks")


# Create Task 
@task_bp.route("", methods=["POST"])
def add_task(): 
    response_body = request.get_json()
    new_task = Task(title=response_body["title"], 
                    description=response_body["description"], 
                    completed_at=response_body["completed_at"]
                    )
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_result()}, 201


# # Get Task Route
# @task_bp.route("", methods=["GET"])
# def get_tasks():
#     response = []
#     all_tasks = Task.query.all()

#     is_complete = True
    
#     if not new_task.completed_at:
#         is_complete = False

#     for task in all_tasks: 
        
    
#     return jsonify(response), 200

# # @task_bp.route("/<", methods=["GET"])
# # def get_tasks():


