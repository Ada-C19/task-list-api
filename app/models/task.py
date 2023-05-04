from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)

#Ver:
# def to_dict(self):
#     return {
#         "id": self.id,
#         "rating": self.rating,
#         "name": self.name,
#         "cuisine": self.cuisine,
#         "distance_from_ada": self.distance_from_ada
#     }
