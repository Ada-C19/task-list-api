from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")
