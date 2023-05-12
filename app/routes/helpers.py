# from flask import abort, make_response, request
# from dotenv import load_dotenv
# load_dotenv()
# import os 
# import requests

# # VALIDATE MODEL
# def validate_model(cls, model_id):
#     try:
#         model_id = int(model_id)
#     except:
#         abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

#     model = cls.query.get(model_id)

#     if not model:
#         abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

#     return model


# def post_to_slack(title):
#     slack_url = "https://slack.com/api/chat.postMessage"
#     API_KEY = os.environ.get("API_KEY")
#     headers = {
#         "Authorization": f"Bearer {API_KEY}"
#     }

#     data = {
#         "channel": "api-test-channel",
#         "text": f"Someone just completed the task {title}"
#     }

#     response = request.post(slack_url, headers=headers, data=data)
#     return response