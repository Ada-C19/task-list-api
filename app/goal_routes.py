from flask import Blueprint, jsonify, request
from app import db
from app import valid
from app.models.goal import Goal


goals_bp = Blueprint('goals', __name__, url_prefix='/goals')


@goals_bp.route('', methods=['POST'])
def create_goal():
    request_body = request.get_json()
    valid_request = valid.validate_entry(Goal, request_body)
    # if 'title' not in request_body:
    #     abort(make_response({'details': 'Invalid data'}, 400))

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