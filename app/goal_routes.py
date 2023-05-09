from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.goal import Goal
from app.routes_helper import validate_item_by_id

# Blueprint for goals
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")