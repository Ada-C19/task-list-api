from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# class Task:
#     def __init__(self, id, title, description, completed_at):
#         self.id = id
#         self.title = title
#         self.description = description
#         self.completed_at = completed_at

# tasks = [
#     Task(1, "Take the dog out", "Dog needs to go pee + poo thrice a day.", "Completed"),
#     Task(2, "Supplemental Studies", "We need to stay ahead of the game! Get studying.", "Completed"),
#     Task(3, "Sweep the floors", "Not just sweep the kitchen + common area, but also vaccuum the rooms.", "Not Complete")
# ] 

#VALIDATE TASKS
# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"message":f"book {task_id} invalid"}, 400))
    
#     for task in tasks:
#         if task.id == task_id:
#             return task
#     abort(make_response({"message":"There's no {task_id} sorry."}))

#POST endpoint CREATES A NEW TASK
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    
    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Made a new task: {new_task.title}", 201)

#GET THE TASKS
# @tasks_bp.route("", methods=["GET"])
# def get_tasks():
#     task_force = []
#     for task in tasks:
#         task_force.append({
#             "id": task.id,
#             "title": task.title,
#             "description": task.description,
#             "completed at":task.completed_at
#         })
#     return jsonify(task_force)

# @tasks_bp.route("/<task_id>", methods=["GET"])
# def handle_tasks(task_id):
#     task = validate_task(task_id)
    
#     return {
#         "id": task.id,
#         "title": task.title,
#         "description": task.description,
#         "completed at":task.completed_at
#         }