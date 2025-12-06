from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import chat, user
from redis_managers.redis_manager import RedisManager
from database import create_tables
import asyncio

redis_manager = RedisManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    # Create database tables
    create_tables()

    # Connect to Redis (optional - app will work without it)
    redis_connected = await redis_manager.connect()

    # Start background task برای گوش دادن به Redis only if connected
    if redis_connected:
        asyncio.create_task(chat.redis_listener())  # تابع redis_listener از chat.py
    else:
        print("Redis not available - chat functionality will be limited")

    yield
    # Shutdown code (اگر نیاز بود)
    print("Shutting down...")

app = FastAPI(title="Test-Newhorizon", lifespan=lifespan)

# Include routers
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
