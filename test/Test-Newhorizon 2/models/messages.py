from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from models.personals import Personal

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("personals.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("personals.id"), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # روابط ORM (اختیاری، برای دسترسی راحت به sender و receiver)
    sender = relationship("Personal", foreign_keys=[sender_id])
    receiver = relationship("Personal", foreign_keys=[receiver_id])

    def __repr__(self):
        return f"<Message(sender_id={self.sender_id}, receiver_id={self.receiver_id}, content={self.content[:20]}...)>"
