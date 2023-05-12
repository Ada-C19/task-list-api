from flask import Blueprint,make_response,request,jsonify,abort
from app import db
from app.models.goal import Goal
from app.helper import validate_goal


#CREATE BP/ENDPOINT
goals_bp = Blueprint("goals",__name__, url_prefix="/goals")


#POST request/response [POST]/goals :(CREATE)
@goals_bp.route("",methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        # if "title" in request_body:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return make_response({"details": "Invalid data"},400)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.to_dict()}),201


#GET one goal [GET]/goals/<id> :(CREATE)
@goals_bp.route("/<id>",methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)

    return jsonify({"goal":goal.to_dict()}),200






