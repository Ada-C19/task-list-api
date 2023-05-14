from app import db

# create task model, define 'Task' using SQLAlchemy 
class Task(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    