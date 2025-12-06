from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.questions import QuestionCreate, QuestionResponse
from models.questions import Question
from database import get_db  # تابعی که session دیتابیس می‌دهد

router = APIRouter()

# ایجاد سوال جدید
@router.post("/", response_model=QuestionResponse)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    if len(question.options) != 4:
        raise HTTPException(status_code=400, detail="Options must have exactly 4 items")
    
    if not (0 <= question.answer <= 3):
        raise HTTPException(status_code=400, detail="Answer must be between 0 and 3")
    
    new_question = Question(
        question=question.question,
        options=question.options,
        answer=question.answer,
        category=question.category
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

# دریافت همه سوالات
@router.get("/", response_model=List[QuestionResponse])
def read_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions

# دریافت یک سوال با id
@router.get("/{question_id}", response_model=QuestionResponse)
def read_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
