from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.messages import MessageResponse, MessageCreate
from services import crud
from database import get_db

router = APIRouter(prefix="/messages", tags=["messages"])

# ارسال پیام جدید از طریق REST
@router.post("/", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    msg = crud.send_message(db, sender_id=message.sender_id, receiver_id=message.receiver_id, content=message.content)
    return msg

# دریافت تمام پیام‌ها بین دو کاربر
@router.get("/{user1_id}/{user2_id}", response_model=List[MessageResponse])
def get_messages(user1_id: int, user2_id: int, db: Session = Depends(get_db)):
    messages = db.query(crud.Message).filter(
        ((crud.Message.sender_id == user1_id) & (crud.Message.receiver_id == user2_id)) |
        ((crud.Message.sender_id == user2_id) & (crud.Message.receiver_id == user1_id))
    ).order_by(crud.Message.timestamp).all()
    return messages
