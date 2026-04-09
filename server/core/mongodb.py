# MongoDB 연결 객체 생성

from pymongo import MongoClient
from core.config import MONGODB_URI, MONGODB_DB_NAME

# MongoDB 클라이언트 생성
mongo_client = MongoClient(MONGODB_URI)

# 사용할 DB 객체
mongo_db = mongo_client[MONGODB_DB_NAME]