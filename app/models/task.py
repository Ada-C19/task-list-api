from app import db

#many tasks
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    # Converts Task model into a dict
    #I have commented out the new to dict attribute from updated Task schema
    def to_dict(self):
        is_complete = False
        if self.completed_at:
            is_complete = True
        dic_data = {
            "id": self.task_id,
            # "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            ####NEEEEED to change this to competed at!!!!!!!!!!!!!!!!!!!!!!!!!!!
            "is_complete": is_complete
        }
        if self.goal_id is not None:
            dic_data["goal_id"] = self.goal_id

        return dic_data
    
    #to_dict that has goals
    def to_dict_with_goal(self):
        is_complete = False
        if self.completed_at:
            is_complete = True
        goal_dic_data = {
            "id": self.task_id,
            # "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
        #if it is not None then we are assinign goal_id to self.goal_id
        #Then it's part of the dictionary and can no correctly be called to include that
        #keyvalue pair.....
        if self.goal_id is not None:
            goal_dic_data["goal_id"]= self.goal_id
        return goal_dic_data




    # Will take in a dict and return a new Task instance
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(
        title= task_data["title"],
        description= task_data['description'],
        completed_at= task_data['completed_at'])

        return new_task
