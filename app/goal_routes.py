from flask import Blueprint, jsonify, request
from app import db
from app import valid
from app.models.goal import Goal


goals_bp = Blueprint('goals', __name__, url_prefix='/goals')