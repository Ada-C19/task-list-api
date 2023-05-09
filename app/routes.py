from app import db
from app.models.task import Task 
from app.models.goal import Goal 
from flask import Blueprint, make_response, abort, request, jsonify
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
load_dotenv()


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")
API_KEY = os.environ.get("API_KEY")

#helper function
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)

    except:
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model 


def post_to_slack(task_title):
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "channel": "task-notification",
        "text": f"Someone just completed the task {task_title}"
    }

    response = requests.post(slack_url, headers=headers, data=data)
    return response



#************Task Routes*****************


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try: 
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()
        return make_response({"task": new_task.to_dict()}, 201)
    except:
        return make_response({"details": "Invalid data"}, 400)


@task_bp.route("", methods=["GET"])
def get_all():
    task_query = Task.query
    title_query = request.args.get("sort")

    if title_query == "asc":
        task_query = Task.query.order_by(Task.title.asc())
    if title_query == "desc":
        task_query = Task.query.order_by(Task.title.desc())

    tasks = task_query.all()
    task_response = [task.to_dict() for task in tasks]

    return jsonify(task_response)



@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return jsonify({"task": task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.is_complete = False

    db.session.commit()

    return make_response(jsonify({
        "task": {
            "id" : task.task_id,
            "title" : task.title,
            "description" : task.description,
            "is_complete" : False
        }
    }), 200)


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task 1 \"{task.title}\" successfully deleted"})), 200



@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()

    db.session.commit()

    post_to_slack(task.title)

    return make_response({"task": task.to_dict()}, 200)


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()

    return {"task": {
    "id": task.task_id,
    "title": task.title,
    "description": task.description,
    "is_complete": False
    }
}

#######GOAL ROUTES ###############


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify(
        {"goal": {
            "id" : new_goal.goal_id,
            "title" : new_goal.title
        }}
    ), 201) 


@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)



@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify({"goal": goal.to_dict()}), 200


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json() 

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({"details" : f"Goal 1 \"{goal.title}\" successfully deleted"})), 200


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.tasks = []
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

    db.session.commit()

    return jsonify({
        "id" : goal.goal_id,
        "task_ids" : request_body["task_ids"]
    })


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_goal(goal_id):

    goal = validate_model(Goal, goal_id)

    goal_dict = {
        "id": goal.goal_id,
        "title": goal.title, 
        "tasks" : [task.to_dict() for task in goal.tasks]
    }

    return jsonify(goal_dict)