from app import db
from flask import abort, make_response
from app.models.goal import Goal
from app.models.task import Task

# Helper functions for Task and Goal Toutes
def validate_model(cls, model_id, required_fields=None):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

def create_model(request_body, cls):
    try:
        new_entity = cls.from_dict(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))
    
    db.session.add(new_entity)
    db.session.commit()

    return new_entity

#helper functions for Goal Routes
def assign_tasks(goal,task_ids):
    new_task_ids = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.goal_id
        new_task_ids.append(task.task_id)
        
        db.session.commit()

    goal.task_ids = new_task_ids
    db.session.commit()

    return new_task_ids


def task_dicts(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = Task.query.filter(Task.goal_id == goal.goal_id)

    task_dicts = []
    for task in tasks:
        task_dict = {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
        task_dicts.append(task_dict)

    return task_dicts