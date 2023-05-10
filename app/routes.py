from flask import Blueprint

tasks_bp = Blueprint("tasks_test_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET"])
def say_hello_world():
    my_beautiful_response_body = "Hello, World!"
    return my_beautiful_response_body, 200