from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Personal(Base):
    __tablename__ = "personals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    friends = Column(JSON, default=[])

    def __repr__(self):
        return f"<Personal(name={self.name}, wins={self.wins}, losses={self.losses}, draws={self.draws})>"
