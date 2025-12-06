import redis.asyncio as redis

class RedisManager:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None  # connection اصلی

    async def connect(self):
        # ایجاد connection اصلی async
        try:
            self.redis = redis.Redis.from_url(self.redis_url)
            # Test the connection
            await self.redis.ping()
            print("Connected to Redis!")
            return True
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")
            print("Application will continue without Redis functionality")
            self.redis = None
            return False

    async def publish(self, channel: str, message: str):
        if self.redis:
            await self.redis.publish(channel, message)

    async def get_pubsub(self):
        # pubsub async درست ایجاد می‌کنیم
        if self.redis:
            pubsub = self.redis.pubsub()
            await pubsub.subscribe("chat")
            return pubsub
        return None
