from app import db
from flask import jsonify


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
