from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db 
from datetime import datetime 


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# helper function to validate_model
# def get_validated_model(cls, model.id):
#     try:
#         model.id = int(model.id)
#     except:
#         abort(make_response({"message":f"Goal {model.id} invalid"}, 400))

#     model = Goal.query.get(model.id)

#     if not model:
#         abort(make_response({"message":f"Goal {model.id} not found"}, 404))

#     return model

# helper function to validate_goal
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"Task {goal_id} invalid"}, 400))

    task = Goal.query.get(goal_id)

    if not task:
        abort(make_response({"message":f"Task {goal_id} not found"}, 404))

    return task


# Routes/Endpoints below 

# create one goal
@goals_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))
    else:
        new_goal = Goal(title=request_body["title"], 
                    description=request_body["description"])

    db.session.add(new_goal)
    db.session.commit()

    response_body = {
        "goal": new_goal.to_dict()
    }

    return response_body, 201


# read/get all goals
@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    sort_request_from_user = request.args.get("sort")
    goals_response = []
    # if user passes in sort as query param, we must check if it is asc or desc
    if sort_request_from_user: 
        if sort_request_from_user == "asc":
            goals = Goal.query.order_by(Goal.title.asc())
        if sort_request_from_user == "desc":
            goals = Goal.query.order_by(Goal.title.desc())

    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response), 200 


# read/get one goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return {"goal": goal.to_dict()}, 200
    # returning as a dict here plus calling to_dict because it's a nested dictionary. If I updated to_dict to handle nested dictionaries it would no longer work for read_all_goals


# update one goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    if request_body["title"]:
        goal.title = request_body["title"]

    if request_body["description"]:
        goal.description = request_body["description"]

    # come back to this!
    # eventually you will need this b/c you will need the option to update this attribute 
    # if request_body["completed_at"]:
    #     goal.completed_at = request_body["completed_at"]

    db.session.add(goal)
    db.session.commit()

    response_body = {
        "goal": goal.to_dict()
    }

    return response_body, 200 


# delete one goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }), 200)




@goals_bp.route("/<goal_id>/mark_complete", methods=["PATCH"])
def patch_goal_as_complete(goal_id):
    goal = validate_goal(goal_id) 

    # updated boolean completed_at for the value associated with is_complete to True by providing a return for current local datetime. This forces it to evaluate to True
    goal.completed_at = datetime.today()

    db.session.commit()

    response_body = {
        "goal": goal.to_dict()
    }

    return response_body, 200


@goals_bp.route("/<goal_id>/mark_incomplete", methods=["PATCH"])
def patch_goal_as_incomplete(goal_id):
    goal = validate_goal(goal_id) 

    # updated boolean completed_at for the value associated with is_complete to False by assigning None. This forces it to evaluate to False
    goal.completed_at = None

    db.session.commit()

    response_body = {
        "goal": goal.to_dict()
    }

    return response_body, 200