from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"details": "Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": "Data not found"}, 404))

    return model

