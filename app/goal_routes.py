from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, make_response, request, abort
from .routes_helper import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}), 400
    # Create a new goal in the database
    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    response_body = dict(goal=new_goal.to_dict())

    return (response_body), 201


@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)
    # goals = Goal.query.all()

    goal_list = [goal.to_dict() for goal in goals]
    return (goal_list), 200


@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    # goal = validate_model(Goal,goal_id)
    # goal = Goal.query.get(goal_id)
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"
        ), 404))

    response_body = dict(goal=goal.to_dict())

    return (response_body), 200


@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    # goal = validate_model(Goal, goal_id)
    # goal = Goal.query.get(goal_id)

    request_body = request.get_json()
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response(dict(details=f"Unknown Goal id: {goal_id}"), 404))

    try:
        goal.title = request_body["title"]
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    response_body = dict(goal=goal.to_dict())

    return (response_body), 200


@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    # goal = validate_model(Goal, goal_id)
    # goal = Goal.query.get(goal_id)
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response(dict(
            details=f"Unknown Goal id: {goal_id}"), 404
        ))

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}, '200 OK')


@goals_bp.post("/<goal_id>/tasks")
def adding_task_ids(goal_id):
    # goal = validate_model(Goal, goal_id)
    # goal = Goal.query.get(goal_id)
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)
    request_body = request.get_json()

    if not goal:
        abort(make_response(dict(details=f"Unknown Goal id:{goal_id}"), 404))

    try:
        task_ids = request_body["task_ids"]
        tasks = []
        for task_id in task_ids:
            # task = Task.query.get(task_id)
            query = db.select(Task).where(Task.task_id == task_id)
            task = db.session.scalar(query)
            if not task:
                abort(make_response(
                    dict(details=f"Unknown Task id: {task_id}"), 404))
            tasks.append(task)

        goal.tasks = tasks
    except KeyError:
        abort(make_response(dict(details="Invalid data"), 400))

    db.session.commit()

    task_ids = [task.task_id for task in tasks]

    response_body = {
        "id": goal.id,
        "task_ids": task_ids

    }
    return make_response(response_body), 200


@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal_id(goal_id):
    # goal = validate_model(Goal, goal_id)
    # goal = Goal.query.get(goal_id)
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        abort(make_response(dict(details=f"Unknown Goal id: {goal_id}"), 404))

    tasks = goal.tasks
    task_list = [task.to_dict() for task in tasks]

    response_body = dict(
        id=goal.id,
        title=goal.title,
        tasks=task_list
    )

    return (response_body), 200
