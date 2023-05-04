from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    #tasks = db.relationship('Task', back_populates = 'Goal', 
#lazy = True)
    tasks = db.relationship('task', backref='goal', lazy=True)


    def to_dict(self):
        goal_as_dict={}
        
        goal_as_dict["id"] = self.goal_id
        goal_as_dict["title"] = self.title
        # if not self.completed_at:
        #     dict_as_dict ["is_complete"] = False
        # else: 
        #     dict_as_dict ["is_complete"] = True
        return goal_as_dict


    @classmethod
    def from_dict(cls, goal_data):
        new_goal =  Goal(title=goal_data["title"], 
                        #completed_at = goal_data["is_complete"]
                        )
        return new_goal
