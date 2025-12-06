from pydantic import BaseModel
from typing import List, Optional

class QuestionBase(BaseModel):
    question: str
    options: List[str]  # باید شامل 4 گزینه باشد
    answer: int  # شماره گزینه صحیح: 0 تا 3
    category: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass  # برای ایجاد سوال جدید همان Base کافی است

class QuestionResponse(QuestionBase):
    id: int  # شناسه دیتابیس

    class Config:
        from_attributes = True  # برای تبدیل خودکار SQLAlchemy object به Pydantic
