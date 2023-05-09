from app import db
from models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")