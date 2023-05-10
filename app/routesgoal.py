from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")
@goal_bp.route("", methods=["POST"])
@goal_bp.route("", methods=["GET"])
@goal_bp.route("", methods=["PUT"])
@goal_bp.route("", methods=["DELETE"])