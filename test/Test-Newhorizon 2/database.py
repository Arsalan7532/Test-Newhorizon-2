from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# مسیر دیتابیس SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# ایجاد engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # فقط برای SQLite
)

# SessionLocal برای dependency در FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base مشترک برای همه مدل‌ها
Base = declarative_base()

# تابع get_db برای Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================
# ایجاد جدول‌ها در دیتابیس
# ============================
# Import models only when creating tables to avoid circular imports
def create_tables():
    from models.personals import Personal
    from models.messages import Message
    from models.questions import Question
    Base.metadata.create_all(bind=engine)

# Note: Tables will be created when the app starts up via lifespan handler
