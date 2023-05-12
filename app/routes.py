from flask import Blueprint,jsonify, abort,make_response,request
from app import db
import requests
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os

task_list_bp = Blueprint("tasks", __name__, url_prefix ="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix = "/goals")

@task_list_bp.route("", methods = ["POST"])
def create_tasks():
    request_body = request.get_json()
    print(request_body)
    print("************")
    
    if (not "title" in request_body) or (not "description" in request_body):
        return{
            "details":"Invalid data"
        }, 400
    try:
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()

        #message = f"Task {new_task.title} successfully created"
        return make_response(jsonify({"task":new_task.task_dict()}), 201)
    
    except KeyError as e:
        abort(make_response("Invalid request. Missing required value: {e}"), 400)

@task_list_bp.route("/<id>", methods = ["GET"])
def get_one_saved_task(id):
    task = validate_task(id)
    return jsonify({"task":task.task_dict()}), 200
 
@task_list_bp.route("", methods = ["GET"])
def get_all_saved_tasks():
    sort_query=request.args.get("sort")
    tasks_query=Task.query
    
    if sort_query =="asc":
        tasks_query = Task.query.order_by(Task.title.asc())
    elif sort_query =="desc":
        tasks_query = Task.query.order_by(Task.title.desc())
    
    tasks = tasks_query.all()

    tasks_response =[task.task_dict() for task in tasks]

    return (jsonify(tasks_response)),200
        
    
    
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    
    task = Task.query.get(task_id)
  
    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task


@task_list_bp.route("/<id>", methods = ["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    response_body = {"task":task.task_dict()}
    
    
    return make_response(jsonify(response_body), 200)

@task_list_bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task= validate_task(id)

    db.session.delete(task)
    db.session.commit()

    message = {"details":f'Task {task.task_id} "{task.title}" successfully deleted'}
    return make_response(jsonify(message), 200)


@task_list_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task=validate_task(id)
    task.completed_at=datetime.now()
    db.session.commit()

    return jsonify({"task":task.task_dict()}), 200



@task_list_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task=validate_task(id)
    task.completed_at=None
    db.session.commit()

    return jsonify({"task":task.task_dict()}), 200

#wave4
def slack_notification():
    url = "https://slack.com/api/chat.postMessage"

    payload = {
    "channel": "api-test-channel",
    "text": "Task completed"
    }
    headers = {
    'Authorization':os.environ.get("SLACK_API_TOKEN")}

    response = requests.post(url, headers=headers, data=payload)

    return response.text
    
#wave 5
@goals_bp.route("",methods=["POST","GET"])
def handle_goal():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return{
                "details": "Invalid data"
            },400

        new_goal = Goal (
            title=request_body["title"]
        )

        db.session.add(new_goal)
        db.session.commit()

        return {
            "goal": {
                "id":new_goal.goal_id,
                "title":new_goal.title
            }
        }, 201

    elif request.method == "GET":
        sorting_goals= request.args.get('sort') 
        list = None
        if sorting_goals== "desc":
            list = Goal.query.order_by(Goal.title.desc()) # descending method
        elif sorting_goals == "asc":
            list = Goal.query.order_by(Goal.title.asc()) # ascending method
        else: 
            list = Goal.query.all()
        goals_response = []
        for goal in list:
            goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
            })
        
        return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET","PUT","DELETE"])
def handle_goal_get(goal_id):
    goal = Goal.query.get(goal_id)
    if goal == None:
        return ("", 404)

    if request.method == "GET":
        return {
            "goal": {
                "id":goal.goal_id,
                "title":goal.title,          
                }
        }
    if request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()

        return jsonify({
            "goal":{
                "id":goal.goal_id,
                "title":goal.title,
            }
        }),200

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()

        return jsonify({
            "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
        }),200


@goals_bp.route("/<goal_id>/tasks", methods=["POST","GET"])
def post_tasked_goal(goal_id):

        goal = Goal.query.get(goal_id)

        if goal == None:
            return (""), 404

        if request.method == "POST":
            request_body = request.get_json()

            tasks_instances= []
            for task_id in request_body["task_ids"]:
                tasks_instances.append(Task.query.get(task_id))

            goal.tasks = tasks_instances

            db.session.commit()

            task_ids = []
            for task in goal.tasks:
                task_ids.append(task.task_id)

            response_body = {
                        "id": goal.goal_id,
                        "task_ids": task_ids
                    }

            return jsonify(response_body), 200

        if request.method == "GET":
            tasks_response =[]
            for task in goal.tasks:
                tasks_response.append({
                    "id": task.task_id,
                    "goal_id": task.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": bool(task.completed_at)
                })
            response_body = {
                "id": goal.goal_id,
                "title": goal.title,
                "tasks" : tasks_response
            }
            return jsonify(response_body), 200

