from app import db
from flask import abort, make_response, jsonify

# Define the Goal class: it represents a goal in the database
class Goal(db.Model):
    # Define the goal_id column as the primary key for the Goal table
    goal_id = db.Column(db.Integer, primary_key=True)
    
    # Define the title column as a string that cannot be null
    title = db.Column(db.String, nullable = False)


    # Establish a one-to-many relationship with the Task model(many tasks)
    # The `tasks` attribute holds a list of Task objects related to this Goal
    # `back_populates` refers to the "goal" relationship defined in the Task model
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    
    
    # Convert a Goal object to a JSON-serializable dictionary
    def to_json(self):
        return{
            "id": self.goal_id,
            "title": self.title
        }
    
    # Update the Goal object's attributes based on the provided request body
    def update_dict(self, request_body):
        self.title = request_body["title"]
    

    # @classmethod decorator indicates that create_dict is a class method associated 
    # with the class itself rather than any particular instance of the class

    # cls parameter: a reference to the class (Goal in this case) and is used 
    # to call the class’s constructor (cls(...)), allowing the method to create a new instance of the class.

    # create_dict method is designed to create a new Goal object using data provided in a dictionary (response_body).
    @classmethod
    # When the create_dict method creates a new Goal object, it does so by calling the class constructor (cls(...))
    def create_dict(cls, response_body):
        try:
            # Create a new Goal object by calling the class constructor (cls(...)) 
            # Extract the "title" value from response_body and pass it to the Goal constructor
            # to set the title attribute of the new Goal instance.
            new_goal = cls(
                title = response_body["title"]
            )
        except KeyError:
            # If the "title" key is missing from the response body, return a 400 error
            abort(make_response(jsonify({"details": "Invalid data"}), 400))                              
        return new_goal
    

