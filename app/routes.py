from flask import Blueprint,jsonify, abort, make_response,request
from app import db
from app.models.task import Task
from app.models.goal import Goal
import datetime



tasks_bp = Blueprint ("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint ("goals", __name__, url_prefix="/goals")

def handle_id_request(cls,id):
    try:
        id = int(id)
    except:
        abort(make_response(jsonify({"message":f"{cls.__name__} {id} invalid"}),400))

    Object = cls.query.get(id)

    if not Object:
        abort(make_response({"message":f"{cls.__name__} {id} not found"},404))
        

    return Object


@tasks_bp.route("", methods=["POST"])

def create_task():

    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"},400)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    task_response = new_task.to_dict()

    return make_response(jsonify ({"task":task_response}), 201)


@tasks_bp.route("", methods=[ "GET"])

def read_all_tasks():

    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        tasks=Task.query.order_by(Task.title.asc())
    elif sorting_query=="desc":
        tasks=Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks: 
        tasks_response.append(task.to_dict())
    
    return make_response(jsonify (tasks_response), 200)

@tasks_bp.route("/<task_id>", methods=["GET"])

def read_one_task(task_id):
    task=handle_id_request(Task, task_id)
    #task = Task.query.get(task_id)

    task_response = task.to_dict()
    return make_response({"task": task_response},200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    
    updated_task=handle_id_request(Task, task_id)
    request_body = request.get_json()

    updated_task.title = request_body["title"]
    updated_task.description = request_body["description"]

    db.session.commit()

    task_response = updated_task.to_dict()

    return make_response(jsonify ({"task":task_response}), 200)

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task= handle_id_request(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f'Task {task.task_id} "{task.title}" successfully deleted'},200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])

def finished_task(task_id):
    
    updated_task=handle_id_request(Task, task_id)

    updated_task.completed_at = datetime.datetime.utcnow()
    db.session.commit()

    task_response = updated_task.to_dict()

    return make_response(jsonify ({"task":task_response}), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])

def unfinished_task(task_id):
    
    updated_task=handle_id_request(Task, task_id)

    updated_task.completed_at = None
    db.session.commit()

    task_response = updated_task.to_dict()
    print (task_response)

    return make_response(jsonify ({"task":task_response}), 200)

@goals_bp.route("", methods=["POST"])

def create_goal():

    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"},400)
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    goal_response = new_goal.to_dict()

    return make_response(jsonify ({"goal":goal_response}), 201)

@goals_bp.route("", methods=[ "GET"])

def read_all_goals():

    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        goals=Goal.query.order_by(Goal.title.asc())
    elif sorting_query=="desc":
        goals=Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    
    goals_response = []
    for goal in goals: 
        goals_response.append(goal.to_dict())
    
    return make_response(jsonify (goals_response), 200)

@goals_bp.route("/<goal_id>", methods=["GET"])

def read_one_goal(goal_id):
    goal=handle_id_request(Goal, goal_id)

    goal_response = goal.to_dict()
    return make_response({"goal": goal_response},200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    
    updated_goal=handle_id_request(Goal, goal_id)
    request_body = request.get_json()

    updated_goal.title = request_body["title"]

    db.session.commit()

    goal_response = updated_goal.to_dict()

    return make_response(jsonify ({"goal":goal_response}), 200)

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    goal= handle_id_request(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'},200)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_one_goals_tasks(goal_id):
    
    goal = handle_id_request(Goal, goal_id)
    request_body = request.get_json()
    if "task_ids" not in request_body:
        return make_response({"details": "Invalid data"},400)
    
    tasks = request_body["task_ids"]
    verified_task_ids=[]

    for task_id in tasks: 
        updated_task=handle_id_request(Task, task_id)
        request_body = request.get_json()
        updated_task.goal_id = goal.goal_id
        verified_task_ids.append(updated_task.task_id)

    db.session.commit()

    return make_response(jsonify ({'id':goal.goal_id,"task_ids":verified_task_ids}), 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_one_goals_tasks(goal_id):
    goal=handle_id_request(Goal, goal_id)

    goal_response = goal.to_dict_with_tasks()

    return make_response(goal_response,200)
    