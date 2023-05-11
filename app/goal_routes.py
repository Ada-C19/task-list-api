from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_reponse, request

goals_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

