from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.goal import Goal

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

