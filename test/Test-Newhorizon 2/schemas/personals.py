from pydantic import BaseModel
from typing import List, Optional

class PersonalBase(BaseModel):
    name: str
    wins: Optional[int] = 0
    losses: Optional[int] = 0
    draws: Optional[int] = 0
    friends: Optional[List[str]] = []

class PersonalCreate(PersonalBase):
    pass  # برای ایجاد کاربر جدید، همان Base کافی است

class PersonalResponse(PersonalBase):
    id: int  # شناسه دیتابیس در پاسخ

    class Config:
        from_attributes = True  # برای تبدیل خودکار SQLAlchemy object به Pydantic
