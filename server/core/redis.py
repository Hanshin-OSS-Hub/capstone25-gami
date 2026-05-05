# redis 연결 관리
import redis
from core.config import REDIS_HOST, REDIS_PORT, REDIS_DB

# redis 서버와 연결된 인스턴스를 생성
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)