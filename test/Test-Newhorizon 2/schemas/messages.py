from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

class MessageCreate(MessageBase):
    pass  # برای ایجاد پیام جدید از همین Base استفاده می‌کنیم

class MessageResponse(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True  # اجازه می‌دهد SQLAlchemy object مستقیم به Pydantic تبدیل شود
