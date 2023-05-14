# from flask import Blueprint, jsonify, abort, make_response, request
# import requests
# from app.models.task import Task
# from app.models.goal import Goal
# from datetime import datetime
# from app import db
# import os

# goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
# tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")



# #POST /tasks
# @tasks_bp.route("", methods=["POST"])
# def create_task():
#     try:
#         request_body = request.get_json()
#         new_task = Task.from_dict(request_body)
#     except KeyError as err:
#         return make_response({"details": "Invalid data"}, 400)

#     db.session.add(new_task)
#     db.session.commit()

#     return jsonify({"task": new_task.to_dict()}), 201
    

# #Validate Model
# def validate_model(cls, task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"details": "Invalid data"}, 400))

#     task = cls.query.get(task_id)

#     if not task:
#         message = {"details": "Invalid data"}
#         abort(make_response(message, 404))

#     return task


# #GET /tasks
# @tasks_bp.route("", methods=["GET"])
# def get_all_tasks():

#     sort_query = request.args.get("sort")

#     if sort_query == "asc":
#         tasks = Task.query.order_by(Task.title)
    
#     elif sort_query == "desc":
#         tasks = Task.query.order_by(Task.title.desc())

#     else:
#         tasks = Task.query.all()
    
#     tasks_response = []
#     for task in tasks:
#         tasks_response.append(task.to_dict())

#     return jsonify(tasks_response), 200


# #GET /tasks/<id>
# @tasks_bp.route("/<task_id>", methods=["GET"])
# def get_one_task(task_id):
#     task = validate_model(Task, task_id)
#     if task:
#         return {"task": task.to_dict()}, 200
    
#     else:
#         return {'details': 'Invalid data'}, 404
    

# #PUT /tasks/<id>
# @tasks_bp.route("<task_id>", methods=["PUT"])
# def update_task(task_id):
#     try:
#         task = validate_model(Task, task_id)
#     except:
#         return jsonify({"Message": "Invalid id"}), 404

#     request_body = request.get_json()

#     task.title = request_body["title"]
#     task.description = request_body["description"]

#     db.session.commit()

#     return jsonify({"task": task.to_dict()}), 200


# #DELETE /tasks/<id>
# @tasks_bp.route("<task_id>", methods=["DELETE"])
# def delete_task(task_id):
#     task = validate_model(Task, task_id)

#     if task is None:
#         return {'details': 'Invalid data'}, 404

#     db.session.delete(task)
#     db.session.commit()

#     message = {"details": f"Task 1 \"{task.title}\" successfully deleted"}
#     return make_response(message, 200)

# #Patch /<task_id>/mark_complete
# @tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"])
# def mark_task_complete(task_id):
#     try:
#         new_task = validate_model(Task, task_id)
#     except:
#         return jsonify({"Message": "Invalid id"}), 404
    
#     new_task.completed_at = datetime.utcnow()

#     send_slack_message(new_task)

#     db.session.commit()

#     return jsonify({"task": new_task.to_dict()}), 200


# @tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_task_incomplete(task_id):
#     try:
#         new_task = validate_model(Task, task_id)
#     except:
#         return jsonify({"Message": "Invalid id"}), 404

#     new_task.completed_at = None
    
#     db.session.commit()

#     return jsonify({"task": new_task.to_dict()}), 200



# def send_slack_message(completed_task):
#     TOKEN = os.environ['SLACK_API_TOKEN']
#     AUTH_HEADERS = {
#         "Authorization": f"Bearer {TOKEN}"
#     }
#     CHANNEL_ID = "C0561UUDX4K"
#     SLACK_URL = "https://slack.com/api/chat.postMessage"

#     try:
#         message = f"Someone just completed the task {completed_task.title}"
#         payload = {
#             "channel": CHANNEL_ID,
#             "text": message
#             }
    
#         requests.post(SLACK_URL, data = payload, headers = AUTH_HEADERS)
    
#     except:
#         print("There was an error making the call to Slack")


# #-----------------------------------------------------------

# @goals_bp.route("", methods=["POST"])
# def create_goal():
#     try:
#         request_body = request.get_json()
#         new_goal = Goal.from_dict(request_body)
#     except KeyError as err:
#         return make_response({"details": "Invalid data"}, 400)

#     db.session.add(new_goal)
#     db.session.commit()

#     return jsonify({"goal": new_goal.to_dict()}), 201


# @goals_bp.route("", methods=["GET"])
# def get_all_goals():

#     goals = Goal.query.all()
    
#     goal_response = []
#     for goal in goals:
#         goal_response.append(goal.to_dict())

#     return jsonify(goal_response), 200


# @goals_bp.route("/<goal_id>", methods=["GET"])
# def get_one_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
#     if goal:
#         return {"goal": goal.to_dict()}, 200
    
#     else:
#         return {'details': 'Invalid data'}, 404
    

# @goals_bp.route("<goal_id>", methods=["PUT"])
# def update_task(goal_id):
#     try:
#         goal = validate_model(Goal, goal_id)
#     except:
#         return jsonify({"Message": "Invalid id"}), 404

#     request_body = request.get_json()

#     goal.title = request_body["title"]

#     db.session.commit()

#     return jsonify({"goal": goal.to_dict()}), 200


# @goals_bp.route("<goal_id>", methods=["DELETE"])
# def delete_goal(goal_id):
#     try:
#         goal = validate_model(Goal, goal_id)

#         db.session.delete(goal)
#         db.session.commit()

#         message = {"details": f"Goal 1 \"{goal.title}\" successfully deleted"}
#         return make_response(message, 200)
    
#     except:
#         return {'details': 'Invalid data'}, 404

# #----------------------------------------------------------

# @goals_bp.route("/<goal_id>/tasks", methods=['POST'])
# def create_goal_with_tasks(goal_id):

#     request_body = request.get_json()
#     goal = validate_model(Goal, goal_id)
#     task_list = request_body.get("task_ids")

#     tasks = []
#     for task_id in task_list:
#         task = validate_model(Task, task_id)
#         task.goal = goal
#         tasks.append(task_id)

#     db.session.commit()

#     message = {
#         "id": goal.goal_id, 
#         "task_ids": tasks
#         }
#     return make_response(message, 200)

        
# @goals_bp.route("/<goal_id>/tasks", methods=['GET'])
# def get_all_tasks_one_goal(goal_id):
#     try:
#         goal = validate_model(Goal, goal_id)
#     except:
#         return make_response({"details": "Invalid data"}, 404)

#     task_list = []

#     for task in goal.tasks:
#         task = validate_model(Task, task.id)
#         task_list.append(task.to_dict())
        
#     message = {
#         "id": goal.goal_id,
#         "title": goal.title,
#         "tasks": task_list
#     }
#     return make_response((message, 200))