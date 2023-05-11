from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app.helper_functions import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

