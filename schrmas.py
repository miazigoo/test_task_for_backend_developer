from datetime import datetime

from pydantic import BaseModel

from database import Base




# Базовая модель для ввода данных
class TaskIn(BaseModel):
    title: str
    description: str
    deadline: str

# Модель для вывода данных
class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime

    class Config:
        from_attributes = True