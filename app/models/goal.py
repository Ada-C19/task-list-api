from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    def to_dict(self):
        #is_complete=True if self.completed_at else False 
        """
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False
        """
        return{
            "id":self.goal_id,
            "title":self.title
        }
    
    #create function for title  
    @classmethod
    def create(cls, request_body):
        return cls(
            title = request_body["title"]
            )
    

#update function for title 
    def update(self, request_body):
        self.title=request_body["title"]
        # self.description=request_body["description"]
        
