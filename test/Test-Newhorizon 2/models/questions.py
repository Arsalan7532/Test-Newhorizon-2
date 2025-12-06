from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)  # لیست 4 گزینه
    answer = Column(Integer, nullable=False)  # شماره گزینه صحیح: 0 تا 3
 # میتوان دسته بندی و درجه سختی سوال هم ایجاد کرد

    def __repr__(self):
        return f"<Question(id={self.id}, question={self.question[:20]}...)>"
