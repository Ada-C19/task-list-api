from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db

# All routes for goals start with "/goals" URL prefix
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({'msg': f"Invalid id '{id}'"}, 400))

    item = model.query.get(id)

    return item if item else abort(make_response({'msg': f"No {model.__name__} with id {id}"}, 404))


