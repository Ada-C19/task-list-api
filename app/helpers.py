from flask import make_response, abort, jsonify

def validate_model(cls, model_id):
        try:
            model_id = int(model_id)
        except ValueError:
            abort(make_response(jsonify({"details": f"{cls.__name__} {model_id} invalid"}), 400))
        
        model = cls.query.get(model_id)
        if not model:
            abort(make_response(jsonify({"details": f"{cls.__name__} {model_id} not found"}), 404))

        return model