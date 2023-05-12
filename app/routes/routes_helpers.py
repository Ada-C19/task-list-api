from flask import abort, make_response
from datetime import datetime


def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} is invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} with id {id} was not found."}, 404))

    return model 


def find_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%m/%d/%y')
    except:
        abort(make_response({"message": f"Invalid date format, please use mm/dd/yy format."}, 400))

    return date_obj 