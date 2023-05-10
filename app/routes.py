from flask import Blueprint, request, make_response, request, abort, jsonify 
from app import db
from app.models.task import Task
from app.models.goal import Goal
# from sqlalchemy import asc, desc
from datetime import datetime
#to call slack api?:
from dotenv import load_dotenv
import requests 
import os
load_dotenv()

# Blueprints:
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    # if "title" not in request_body or "description" not in request_body :
    if not "title" in request_body or not "description" in request_body:
        return make_response({"details": "Invalid data"}, 400)
        # abort(make_response({"details": "Invalid data"}, 400))
    if not "completed_at" in request_body:
        request_body["completed_at"] = None

    #Replacing this with the from_dict in task.py
    # new_task = Task(
    #         title= request_body["title"],
    #         description= request_body['description'],
    #         completed_at= request_body['completed_at']
    #     )
    new_task = Task.from_dict(request_body)

    
    db.session.add(new_task)
    db.session.commit()

    is_complete = False
    if new_task.completed_at:
        is_complete = True

    # print(f"new_task.todict {new_task.to_dict}")

    return {"task": new_task.to_dict()}, 201
    # return {
    #     "task": {
    #         "id": new_task.task_id,
    #         "title": new_task.title,
    #         "description": new_task.description,
    #         "is_complete": is_complete
    #     }
    # }

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []

    ### Creating the query Params######
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        total_tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        total_tasks = Task.query.order_by(Task.title.desc()).all()
    else:
    ####End of Query#############
        total_tasks = Task.query.all()
    
    for task in total_tasks:
        # tasks_response.append({
        #     "id": task.task_id,
        #     "title": task.title,
        #     "description": task.description,
        #     "is_complete": False
        # })
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=['GET'])
def read_one_task(task_id):
    # task = Task.query.get(task_id)
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    # is_complete = False
    # if task.completed_at:
        # is_complete = True

    # return {"task":{
    #     "id": task.task_id, 
    #     "title": task.title,
    #     "description": task.description,
    #     # "is_complete": False
    #     "is_complete": is_complete
    # }
    # }, 200
    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    # task = Task.query.get(task_id)
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]


    db.session.commit()

    is_complete = False
    if task.completed_at:
        is_complete = True

    return {"task":{
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        # "is_complete": False,
        "is_complete": is_complete
    }
    }, 200

######GET CLARIFICATION ON THE RETURN MESSAGE
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    # task = Task.query.get(task_id)
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

# return {
#   "details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
# },
#make response returnse a status code 200
# return make_response({
#     "details": "Task {task.task_id}"
# })

    # return make_response(f"Task {task.task_id} successfully deleted")
    return {
        "details": f'Task {task_id} \"{task.title}\" successfully deleted'
    }, 200
    
# Working validation
# def validate_item(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"message": f"invalid task_id: {task_id}"}, 400))
    
#     task = Task.query.get(task_id)

#     if not task:
#         abort(make_response({"message": f"task {task_id} not found"}, 404))

#     return task

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task(task_id):
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()

    db.session.commit()

    is_complete = True

    # Calling the Slack API
    ana_bot = {
        "token": os.environ.get("SLACKBOT_TOKEN_API"),
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title} :clap:"
    }

    requests.post(url="https://slack.com/api/chat.postMessage", data = ana_bot)
    # End of Slack API call

    return {"task":{
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete
    }
    }, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(task_id):
    # task = validate_item(task_id)
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    is_complete = False 

    return {"task":{
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete
    }
    }, 200

# CRUD for Goals
@goals_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    if not "title" in request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals_response = []

    #Get all
    total_goals = Goal.query.all()

    for goal in total_goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200
    
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": {
        "id": goal.goal_id,
        "title": goal.title
    }}, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    },200


# Nested Routes one(Goal) to many(tasks) relationships
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body=request.get_json()

    list_task_ids = request_body["task_ids"]
    
    for task_id in list_task_ids:
        #instance of Task
        task = validate_model(Task, task_id)
        #instance of task. setting it's goal_id = goal_id that's being passed in
        task.goal_id = goal_id
        db.session.commit()

    return{
        "id": goal.goal_id,
        "task_ids": list_task_ids
    }, 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_list = []
    
    # all_tasks = Task.query.all()

    # for task_instance in all_tasks:
    #     if task_instance.goal_id == goal.goal_id:
    #         task_list.append(task_instance.to_dict_with_goal())

    # return {
    #     "id": goal.goal_id,
    #     "title": goal.title,
    #     "tasks": task_list
    # }

    print(goal.tasks)

    for task in goal.tasks:
        response =task.to_dict()
        # response = task.to_dict_with_goal()
        task_list.append(response)


    return {
        "id": goal.goal_id, 
        "title": goal.title,
        "tasks": task_list
    }, 200

    # tasks_response= []
    # response_body={}
    # for task in goal.tasks:
    #     tasks_response.append(task.to_dict_with_goal())

    # response_body["id"]= goal.goal_id
    # response_body["title"] = goal.title  
    # response_body["tasks"] = tasks_response

    # return jsonify(response_body), 200







#passing 1 test
    # for task in goal.tasks:
    #     is_complete = False
    #     if task.completed_at:
    #         is_complete = True
    #     task_list.append({
    #         "id": task.task_id,
    #         "goal_id": goal.goal_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": is_complete
    #     })

    # return {
    #     "id": goal.goal_id,
    #     "title": goal.title,
    #     "tasks": task_list
    # }


    # all_tasks = goal.tasks

    # for task in all_tasks:
    #     # task_list_goal = 
    #     task_list.append(task.to_dict_with_goal())
    # # gives me a list of nulls....so....progress
    # # return jsonify(task_list), 200
    # return {
    #     "id": goal.goal_id,
    #     "title": goal.title,
    #     "tasks": task_list
    # }, 200


    # #or can use something like this:
    # #and inside the () we can call the goal.task_id
    # # total_tasks = Task.query.limit(goal_id).all()

    # ###ask my db that have that goal and then return in reponse

    # # return({"tasks": total_tasks}), 200
    # return make_response(goal.to_dict_with_goal(), 200)

    # Goal.query.get(goal_id).tasks




