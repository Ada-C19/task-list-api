from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import datetime
from typing import Optional

class Task(db.Model):
    task_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime.datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")
    # goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):

        task_dict = dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = self.completed_at != None,
        )
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    @classmethod
    def from_dict(cls, data_dict):

        return cls(
            title = data_dict["title"],
            description = data_dict["description"]
        )