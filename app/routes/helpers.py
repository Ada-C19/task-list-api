from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from app import db
import os


def validate_model(cls, task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    task = cls.query.get(task_id)

    if not task:
        message = {"details": "Invalid data"}
        abort(make_response(message, 404))

    return task