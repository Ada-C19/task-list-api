from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from app import db
import os


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        message = {"details": "Invalid data"}
        abort(make_response(message, 404))

    return model

def create_item(cls):
    try:
        request_body = request.get_json()
        new_item = cls.from_dict(request_body)
    except KeyError as err:
        return make_response({"details": "Invalid data"}, 400)
    
    db.session.add(new_item)
    db.session.commit()
        
    return make_response({cls.__name__.lower(): new_item.to_dict()}, 201)


def get_all_items(cls):

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        items = cls.query.order_by(cls.title)
    
    elif sort_query == "desc":
        items = cls.query.order_by(cls.title.desc())

    else:
        items = cls.query.all()

    if request.args.get("title"):
        items = cls.query.filter(cls.title== request.args.get("title"))

    items_response = []
    for item in items:
        items_response.append(item.to_dict())

    return jsonify(items_response), 200


def get_one_item(cls, model_id):

    item = validate_model(cls, model_id)

    if item:
        return make_response({cls.__name__.lower(): item.to_dict()}), 200
    
    else:
        return {'details': 'Invalid data'}, 404
    


def update_item(cls, model_id):
    
    item = validate_model(cls, model_id)
    request_body = request.get_json()
    
        # return jsonify({"Message": "Invalid id"}, 404)
    
    for key, value in request_body.items():
        setattr(item, key, value)

    db.session.commit()

    return jsonify({cls.__name__.lower(): item.to_dict()}, 200)

#--------------------------------------------

