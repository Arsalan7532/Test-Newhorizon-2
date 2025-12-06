from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.personals import PersonalCreate, PersonalResponse
from models.personals import Personal, Base
from database import get_db  # تابعی که session دیتابیس می‌دهد

router = APIRouter()

# ایجاد کاربر جدید
@router.post("/", response_model=PersonalResponse)
def create_personal(personal: PersonalCreate, db: Session = Depends(get_db)):
    # بررسی اینکه نام تکراری نباشد
    existing = db.query(Personal).filter(Personal.name == personal.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Name already exists")
    
    new_personal = Personal(
        name=personal.name,
        wins=personal.wins,
        losses=personal.losses,
        draws=personal.draws,
        friends=personal.friends
    )
    db.add(new_personal)
    db.commit()
    db.refresh(new_personal)
    return new_personal

# دریافت همه کاربران
@router.get("/", response_model=List[PersonalResponse])
def read_personals(db: Session = Depends(get_db)):
    personals = db.query(Personal).all()
    return personals

# دریافت یک کاربر با id
@router.get("/{personal_id}", response_model=PersonalResponse)
def read_personal(personal_id: int, db: Session = Depends(get_db)):
    personal = db.query(Personal).filter(Personal.id == personal_id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal not found")
    return personal
