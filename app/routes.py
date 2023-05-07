from flask import Blueprint,jsonify, request
from app import db

tasks_bp = Blueprint("books", __name__, url_prefix="/tasks")

def create_task():
    request_body = request.get_json()

    new_task = Task()
