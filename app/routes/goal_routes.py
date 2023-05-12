from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
from app.helpers import validate_model
import os
import requests

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

