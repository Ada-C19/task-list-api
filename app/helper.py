from flask import abort, make_response
from app.models.task import Task
from app.models.goal import Goal


def validate_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"this is not a valid id: {id}"}, 400))
    
    task = Task.query.get(id)
    if not task:
        abort(make_response({"message":f"id {id} not found!"}, 404))
    return task

def validate_goal(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"this is not a valid id: {id}"}, 400))
    
    goal = Goal.query.get(id)
    if not goal:
        abort(make_response({"message":f"id {id} not found!"}, 404))
    return goal


