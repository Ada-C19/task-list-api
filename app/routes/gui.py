from flask import Blueprint, render_template, send_from_directory

gui_bp = Blueprint("gui", __name__, url_prefix="/")

@gui_bp.route("", methods=["GET"])
def index():  
    return render_template('index.html')