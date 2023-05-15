from app import db
from flask import jsonify, make_response, abort 

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)

    
    def to_dict(self):
        task_dict = dict(
                id = self.task_id,
                title = self.title,
                description = self.description
            )   

        if self.completed_at:
            task_dict["is_complete"] = True 

        else: 
            task_dict["is_complete"] = False

        return task_dict 
    
    @classmethod
    def from_dict(cls, data_dict): 
        try: 
            new_cls = cls(
                    title = data_dict["title"],
                    description = data_dict["description"] 
                ) 
        except KeyError:
            
            abort(make_response(jsonify({"details": "Invalid data"}), 400))
            
        return new_cls


