from flask import abort, make_response, request, jsonify
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import timezone, datetime
from http import HTTPStatus


def validate_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        error_message = generate_error_message(cls, model_id)
        abort(make_response(error_message, HTTPStatus.BAD_REQUEST))
    return model_id


def get_model_by_id(cls, model_id):
    model_id = validate_id(cls, model_id)
    model = db.session.get(cls, model_id)

    if not model:
        error_message = generate_error_message(cls, model_id)
        abort(make_response(error_message, HTTPStatus.NOT_FOUND))  
        
    return model

def generate_error_message(cls, model_id):
    return {"message": f"{cls.__name__} {model_id} was not found."}


def create_instance(cls):
    request_body = request.get_json()

    instance = cls.from_json(request_body)

    db.session.add(instance)
    db.session.commit()

    instance = instance.to_json()
    cls_type = cls.__name__.lower()

    return make_response(jsonify({cls_type: instance}), HTTPStatus.CREATED)


def get_all_instances(cls):
    instances = cls.query.all()

    instance_list = [instance.to_json() for instance in instances]

    return make_response(jsonify(instance_list), HTTPStatus.OK)


def get_one_instance(cls, model_id):
    instance = get_model_by_id(cls, model_id)

    instance = instance.to_json()
    cls_type = cls.__name__.lower()
    
    return make_response(jsonify({cls_type: instance}), HTTPStatus.OK)








# @tasks_bp.route("/<task_id>", methods=['PUT'])
# def update_task(task_id):
#     task = get_task_by_id(task_id)
#     updated_task = update_task_from_request(task, request)

#     db.session.commit()

#     task = updated_task.to_json()

#     return make_response(jsonify(task=task)), 200





# def validate_data(request):
#     instance_info = request.get_json()
#     if not "title" in instance_info or not "description" in instance_info:
#         abort(make_response({"details": "Invalid data"}, 400))
#     instance_info["completed_at"] = instance_info.get("completed_at")
#     return instance_info







 

# def update_task_from_request(task, request):
#     task_info = request.get_json()

#     if 'title' in task_info:
#         task.title = task_info['title']
#     if 'description' in task_info:
#         task.description = task_info['description']
#     if 'completed_at' in task_info:
#         task.completed_at = task_info['completed_at']
#     else:
#         task.completed_at = None

#     return task

# def get_goal_instance(request):
#     goal_info = validate_goal_data(request)
#     return Goal.from_json(goal_info)

# def validate_goal_id(goal_id):
#     try:
#         goal_id = int(goal_id)
#     except:
#         abort(make_response({"message": f"Invalid goal ID: {goal_id}"}, 400))

#     return goal_id

# def get_goal_by_id(goal_id):
#     goal_id = validate_goal_id(goal_id)
#     goal = db.session.get(Goal, goal_id)

#     if not goal:
#         abort(make_response({'message': f'Goal {goal_id} was not found.'}, 404))
        
#     return goal 

# def update_goal_from_request(goal, request):
#     goal_info = request.get_json()

#     if 'title' in goal_info:
#         goal.title = goal_info['title']

#     return goal

# def validate_goal_data(request):
#     goal_info = request.get_json()
#     if not "title" in goal_info:
#         abort(make_response({"details": "Invalid data"}, 400))
#     return goal_info
