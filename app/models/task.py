from app import db
# from collections import OrderedDict


# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String)
#     description = db.Column(db.String)
#     completed_at = db.Column(db.DateTime, nullable= True)
#     is_complete = db.Column(db.Boolean, default=False)

#     # @classmethod
#     # def from_dict(cls, data_dict):
#     #     return cls(
#     #         title=data_dict["title"],
#     #         description=data_dict["description"],
#     #         is_complete=data_dict["is_complete"]
#     #     )

#     def to_dict(self):
#             return (dict(
#                 id=self.id,
#                 title=self.title,
#                 description=self.description,
#                 is_complete=self.is_complete
#             ))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        if not self.completed_at:
            self.is_complete = False
        return (dict(
                id=self.id,
                title=self.title,
                description=self.description,
                is_complete=self.is_complete
            ))
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"],
            description = data_dict["description"],
            is_complete = data_dict["completed_at"]
        )
