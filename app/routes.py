from flask import Blueprint,jsonify, request, make_response, abort
import requests
from app.models.task import Task
from app.models.goal import Goal
from app import db
import datetime
import os


task_bp = Blueprint("tasks", __name__,url_prefix="/tasks")

#post a task
@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Bad Request"}, 400
    
    new_task = Task.from_dict(request_body)
    


    db.session.add(new_task)
    db.session.commit()

    return {"task" : new_task.to_dict()}, 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    response = []
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        all_tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        all_tasks = Task.query.order_by(Task.title.desc())
    else:
        all_tasks = Task.query.all()

    for task in all_tasks:
        response.append(task.to_dict())

    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_id(Task,task_id)

    return {"task" : task.to_dict()}, 200

@task_bp.route("<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)

    request_data = request.get_json()

    task.title = request_data["title"]
    task.description = request_data["description"]

    db.session.commit()

    return {"task" : task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_not_complete(task_id):
    task = validate_id(Task, task_id)

    task.completed_at = None
    
    db.session.commit()
    return {"task" : task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task__is_complete(task_id):
    task = validate_id(Task, task_id)
    # request_data = request.get_json()

    task.completed_at = datetime.datetime.now()
    
    db.session.commit()

    token = os.environ.get("TOKEN")
    url = "https://slack.com/api/chat.postMessage"
    channel = "task-notification"
    text = "GOOD JOB"
    workspace= {"token": token, "channel": channel, "text" :text}


    requests.post(url=url,data=workspace)

    return {"task" : task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}

def validate_id(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"msg": "bad request"},400))
    
    item = model.query.get(item_id)
    if not item:
        return abort(make_response({"msg": "invalid endpoint"},404))
    
    return item



goal_bp = Blueprint("goals", __name__, url_prefix="/goals")
@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return {"details": "Bad Request"}, 400
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    response = []
    title_query = request.args.get("title")

    if title_query is None:
        all_goals = Goal.query.all()
    else:
        all_goals = Goal.query.filter_by(title=title_query)

    for goal in all_goals:
        response.append(goal.to_dict())

    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_id(Goal,goal_id)

    return {"goal" : goal.to_dict()}, 200

@goal_bp.route("<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    goal = validate_id(Goal, goal_id)

    request_data = request.get_json()

    goal.title = request_data["title"]

    db.session.commit()

    return {"goal" : goal.to_dict()}, 200

@goal_bp.route("/<goal_id>",methods=["DELETE"])
def delete_goal(goal_id):

    goal = validate_id(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}





@goal_bp.route("<goal_id>/tasks", methods=["POST"])
def add_task_to_goal(goal_id):
    goal =validate_id(Goal,goal_id)
    request_body = request.get_json()

    task_ids = request_body["task_ids"]

    for task_id in task_ids:
        task = validate_id(Task,task_id)

        task.goal = goal

    # db.session.add(task)
    db.session.commit()

    return jsonify ({"id": goal.goal_id, "task_ids": task_ids}), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_of_goal(goal_id):
    goal = validate_id(Goal,goal_id)

    
    

    print("LKJSALDFJSADLF**********")
    print('goal.tasks, do you exist? what do you return?', goal.tasks)
    print(goal.tasks[0])
    print(goal.tasks[0].to_dict())
    print("******")


    return ({"id": goal.goal_id,"title": goal.title, "tasks": [] }), 200