import redis.asyncio as redis
import os

#redis setup, using radis library for async operations

host = os.getenv("REDIS_HOST", "localhost")
port = os.getenv("REDIS_PORT", 6379)
db = os.getenv("REDIS_DB", 0)

redis_client = redis.Redis(
    host=host,
    port=port,
    db=db
)
