from sqlalchemy import Column, Integer, String, DateTime

from database import Base


# Модель таблицы задач
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    deadline = Column(DateTime)