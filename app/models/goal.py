from app import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    task = db.relationship("Task", back_populates="goal")
