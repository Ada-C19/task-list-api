from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import datetime
from typing import Optional


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    # tasks: Mapped[Optional["Task"]] = relationship("Task", back_populates="goal")

    def to_dict(self):
        goal_dict=dict(
        id = self.id,
        title = self.title
        )
        return goal_dict