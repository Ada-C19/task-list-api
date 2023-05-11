from flask import Blueprint, jsonify, request
from app import db
from app import valid
from app.models.goal import Goal
from app.models.task import Task


goals_bp = Blueprint('goals', __name__, url_prefix='/goals')


@goals_bp.route('', methods=['POST'])
def create_goal():
    request_body = request.get_json()
    valid_request = valid.validate_entry(Goal, request_body)

    new_goal = Goal.from_dict(valid_request)
    
    db.session.add(new_goal)
    db.session.commit()
    return {'goal': new_goal.to_dict()}, 201


@goals_bp.route('', methods=['GET'])
def get_goals():
    title_query = request.args.get('title')
    
    if title_query:
        goals = Goal.query.filter(Goal.title.ilike('%'+title_query.strip()+'%'))
    else:
        goals = Goal.query.all()
    
    goal_response = [goal.to_dict() for goal in goals]
    return jsonify(goal_response), 200


@goals_bp.route('/<goal_id>', methods=['GET'])
def get_goal_by_id(goal_id):
    goal = valid.validate_id(Goal, goal_id)
    
    return {'goal': goal.to_dict()}, 200


@goals_bp.route('/<goal_id>', methods=['PUT'])
def replace_goal(goal_id):
    goal = valid.validate_id(Goal, goal_id)
    
    request_body = request.get_json()
    valid_request = valid.validate_entry(Goal, request_body)
    
    goal.title = valid_request['title']
    
    db.session.commit()
    return {'goal': goal.to_dict()}, 200

@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = valid.validate_id(Goal, goal_id)
    
    goal_title = goal.title
    
    db.session.delete(goal)
    db.session.commit()
    return {'details': f'Goal {goal_id} "{goal_title}" successfully deleted'}, 200

# relantionship routes
@goals_bp.route('/<goal_id>/create_task', methods=['POST'])
def create_task_assigned_to_specific_goal(goal_id):
    goal = valid.validate_id(Goal, goal_id)
    request_body = request.get_json()
    
    valid_request = valid.validate_entry(Task, request_body)
    
    new_task = Task.from_dict_with_parent(valid_request, goal_id)
    
    db.session.add(new_task)
    db.session.commit()
    return {'details': f'New task "{new_task.title}" for goal "{goal.title}" created', 'task details': new_task.to_dict()}, 201

@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def create_list_of_tasks_to_goal(goal_id):
    valid.validate_id(Goal, goal_id)
    request_body = request.get_json()

    tasks_response = [Task.from_dict_with_parent(task, goal_id) for task in request_body if valid.validate_entry(Task, task)]
    
    db.session.add_all(tasks_response)
    db.session.commit()
    return {'id': goal_id, 'task_ids': [task.id for task in tasks_response]}, 201

@goals_bp.route('/<goal_id>/tasks/<task_id>', methods=['PATCH'])
def match_task_with_goal(goal_id, task_id):
    goal = valid.validate_id(Goal, goal_id)
    task = valid.validate_id(Task, task_id)
    
    task.goal_id = goal_id

    db.session.commit()
    
    return {'details': f'Task "{task.title}" assigned to goal {goal_id} "{goal.title}" successfully'}, 200
