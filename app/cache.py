import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def get_cache(key: str):
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"Cache GET error: {e}")
        return None

def set_cache(key: str, value: dict, expire_seconds: int = 60):
    try:
        redis_client.setex(key, expire_seconds, json.dumps(value))
        print(f"Cache SET: {key}")
    except Exception as e:
        print(f"Cache SET error: {e}")

def delete_cache(key: str):
    try:
        redis_client.delete(key)
    except Exception:
        pass

def clear_execution_cache():
    try:
        for key in redis_client.scan_iter("executions:*"):
            redis_client.delete(key)
        for key in redis_client.scan_iter("summary:*"):
            redis_client.delete(key)
    except Exception:
        pass