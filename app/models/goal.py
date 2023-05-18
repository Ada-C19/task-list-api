from app import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(56))
    task = db.relationship("Task", backref="goal", lazy=True)
    
    def to_dict(self):
        return{
            "id": self.id,
            "title": self.title,
        }
