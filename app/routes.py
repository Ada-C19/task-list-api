from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


load_dotenv()
task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")


#helper function

def validate_task(model, task_id):
    try:
        task_id = int(task_id)

    except ValueError:
        return abort(make_response({
            "error": f"invalid id {task_id} not found"}, 400
        ))

    task = model.query.get(task_id)
    if task is None:
        abort(make_response({
            "error": "task not found"}, 404
        ))
    return task


def validate_goal(model, goal_id):
    try:
        goal_id = int(goal_id)

    except ValueError:
        return abort(make_response({
            "error": f"invalid id {goal_id} not found"}, 400
        ))

    task = model.query.get(goal_id)
    if task is None:
        abort(make_response({
            "error": "goal not found"}, 404
        ))
    return task

#WAVE 1

#CREATE
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    #using class method - from_dict() from Task model
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return jsonify(
        {"task":new_task.task_to_dict()
        
    }), 201



# #GET ONE
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

#check if task_id exists
    task = validate_task(Task, task_id)

    return jsonify({"task": task.task_to_dict()}), 200

#Update
@task_bp.route("/<id>", methods=["PUT"])
def update_task(id):

    task = validate_task(Task, id)
    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]
    task.completed_at = request_data.get("completed_at", None)

    db.session.commit()

    return jsonify({"task": task.task_to_dict()}), 200

#Delete
@task_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):

    task = validate_task(Task, id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {id} "Go on my daily walk 🏞" successfully deleted'}, 200




# #WAVE 2


@task_bp.route("", methods=["GET"])
def get_all_and_sort_title():

    response = []

    query = request.args.get("sort")

#check whether asc or desc
    if query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        #otherwise, get all
        tasks = Task.query.all()

    for each_task in tasks:
        response.append(each_task.task_to_dict())

    return jsonify(response), 200


#Mark InComplete
@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(task_id):
    task = validate_task(Task, task_id)

    task = Task.query.get(task_id)
    
    #sets the task to incomplete regardless if it's complete or incomplete
    task.completed_at = None
    db.session.commit()
    

    return jsonify(
        {"task": task.task_to_dict()}
    ), 200

#Mark Complete
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task(task_id):
    task = validate_task(Task, task_id)

    task = Task.query.get(task_id)

#sets the current date 
    task.completed_at = datetime.now()
    db.session.commit()

    #slack start
    slack_token = os.environ.get("SLACK_API_TOKEN")
    slack_message = f"Somone just completed the task {task.title}"
    slack_client = WebClient(token=slack_token)

    try:
        response = slack_client.chat_postMessage(
            channel = "task-notifications",
            text=slack_message
        )
    except SlackApiError as error:
        print(f"error {error}")

    return jsonify({
        "task": task.task_to_dict()
    }), 200

#START OF GOAL

#CREATE
@goal_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({
            "details": "Invalid data"
        }
        ), 400
    
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return jsonify(
        {
            "goal": new_goal.goal_to_dict()
        }), 201


#GET ALL
@goal_bp.route("", methods = ["GET"])
def get_all_goals():
    response = []

    goals = Goal.query.all()

    for each_goal in goals:
        response.append(each_goal.goal_to_dict())

    return jsonify(response), 200

#GET ONE
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):

    goal = validate_goal(Goal, goal_id)
    

    return jsonify({
        "goal": goal.goal_to_dict()
    }), 200

#UPDATE
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    goal = validate_goal(Goal, goal_id)
    request_data = request.get_json()

    goal.title = request_data["title"]

    db.session.commit()

    return jsonify({
        "goal": goal.goal_to_dict()
    }), 200

#DELETE
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

    goal = validate_goal(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return{
        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }, 200


#ONE TO MANY
@goal_bp.route("/<int:goal_id>/tasks", methods=["POST"])
def get_tasks_list(goal_id):

    goal = validate_goal(Goal, goal_id) #goal_id 7

    request_data = request.get_json()
    task_ids_list = request_data["task_ids"]  #[1,2,3]

    for each_task_id in task_ids_list:
        task_obj = Task.query.get(each_task_id) #get elem in database
        
     
        task_obj.goal_id = goal_id #set the goal_id as the task_data's goal_id
        db.session.commit()
     
    return jsonify(
        {
            "id": goal_id,
            "task_ids": task_ids_list
        }
    ), 200

#GET GOAL
@goal_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_for_specific_goal(goal_id):
    goal = validate_goal(Goal, goal_id)

#this returns a list of all tasks instances that has the goal_id
    tasks_obj_list = Task.query.filter_by(goal_id = goal_id).all()

#checking if tasks is empty
    if not tasks_obj_list:
        return jsonify(
            {
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": []
            })
    #insert this to pass tasks for specific goal - second to last
  
    task_list = []
    for each_task in tasks_obj_list:
        task_list.append(each_task.task_to_dict())
        
    return jsonify(
        {
            "id":goal.goal_id,
            "title": goal.title,
            "tasks": task_list
        }
    ), 200

#comment out when passing second to last
    # for each_task in tasks_obj_list:
    #     return jsonify(
    #         {"tasks": each_task.task_to_dict()}
    #     ), 200




