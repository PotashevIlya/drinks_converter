from sqlalchemy import Column, Integer, String

from app.core.db import Base


class Drink(Base):
    name = Column(String(50), unique=True, nullable=False)
    average_strength = Column(Integer, nullable=False)

    def __repr__(self):
        return f'{self.name}, средняя крепость - {self.average_strength}.'
