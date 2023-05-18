from app import db

# create task model, define 'Task' using SQLAlchemy 
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(56))
    description = db.Column(db.String(200))
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)

