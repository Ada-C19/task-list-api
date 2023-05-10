from flask import make_response, abort

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model




# def validate_goal(id):
#     try:
#         id = int(id)
#     except:
#         abort(make_response({"message": f"Goal {id} is invalid"}, 400))

#     goal = Goal.query.get(id)

#     if not goal:
#         abort(make_response({"message": f"Goal {id} not found"}, 404))

#     return goal