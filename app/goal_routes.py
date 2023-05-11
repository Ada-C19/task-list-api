from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_task(cls,goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {goal_id} invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"message":f"{cls.__name__} {goal_id} not found"}, 404))
    return goal

# POST request to create new goal
@goals_bp.route("", methods=['POST'])
def create_goal():
    request_body = request.get_json()   
    try: 
        new_goal = Goal.from_dict(request_body)
    except:
        return {"details": "Invalid data"}, 400
    

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    sort_goals = request.args.get('sort')

    if sort_goals == 'asc':
        goals = Goal.query.order_by(Goal.title.asc()).all()
    elif sort_goals == 'desc':
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_by_id(goal_id):
    goal = validate_task(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_task(goal_id):
    goal_to_update = validate_task(Goal, goal_id)

    request_body = request.get_json()
  
    goal_to_update.title = request_body["title"]

    db.session.commit()
    

    return {"goal": goal_to_update.to_dict()}, 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_task(goal_id):
    goal = validate_task(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()

    return{
        "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    }, 200
