from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id_parent = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))

    @classmethod
    def from_dict(cls, data_dict, goal=None):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            goal=goal
        )

    def to_dict(self):
        dictionary={}
        if self.goal:
            dictionary=dict(
            id=self.id,
            title=self.title,
            description=self.description,
            goal_id=self.goal_id_parent,
            is_complete=self.completed_at != None
        )      
        else:
            dictionary=dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at != None
        )        
            
        return dictionary
    
 