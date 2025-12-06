from sqlalchemy.orm import Session
from models.personals import Personal
from models.messages import Message  # فرض می‌کنیم یک مدل Message هم داریم
from schemas.personals import PersonalCreate
from typing import Optional, List

# ==========================
# کاربران (Personal)
# ==========================

def create_user(db: Session, user: PersonalCreate) -> Personal:
    """ایجاد کاربر جدید"""
    existing = db.query(Personal).filter(Personal.name == user.name).first()
    if existing:
        raise ValueError("User with this name already exists")
    
    db_user = Personal(
        name=user.name,
        wins=user.wins,
        losses=user.losses,
        draws=user.draws,
        friends=user.friends
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: Optional[int] = None, name: Optional[str] = None) -> Optional[Personal]:
    """دریافت کاربر بر اساس id یا name"""
    query = db.query(Personal)
    if user_id is not None:
        return query.filter(Personal.id == user_id).first()
    elif name is not None:
        return query.filter(Personal.name == name).first()
    return None


# ==========================
# پیام‌ها (Message)
# ==========================

def send_message(db: Session, sender_id: int, receiver_id: int, content: str) -> "Message":
    """
    ذخیره پیام بین کاربران
    فرض می‌کنیم مدل Message داریم:
    sender_id, receiver_id, content, timestamp
    """
    db_message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
