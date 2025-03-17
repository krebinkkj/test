import zlib
import pickle
from functools import lru_cache
from datetime import datetime
import redis
from sqlalchemy.orm import Session
from database.models import MemoryRecord
from database.session import get_db
from config import config

class HybridMemory:
    def __init__(self):
        self.redis = redis.Redis.from_url(config.REDIS_URL)
        self.db = next(get_db())
        
    @lru_cache(maxsize=1024)
    def get(self, key: str):
        # Tenta primeiro no Redis
        if cached := self.redis.get(key):
            return self._deserialize(cached)
            
        # Busca no banco SQL
        if record := self.db.query(MemoryRecord).filter(MemoryRecord.id == key).first():
            self.redis.setex(key, 3600, record.data)
            return self._deserialize(record.data)
            
        return None

    def store(self, key: str, data: object, ttl: int = 86400):
        serialized = self._serialize(data)
        
        # Armazena no Redis
        self.redis.setex(key, ttl, serialized)
        
        # Armazena no SQL
        record = MemoryRecord(
            id=key,
            data=serialized,
            timestamp=datetime.now().timestamp()
        )
        self.db.merge(record)
        self.db.commit()
        self.get.cache_clear()

    def _serialize(self, data: object) -> bytes:
        return zlib.compress(pickle.dumps(data))
        
    def _deserialize(self, data: bytes) -> object:
        return pickle.loads(zlib.decompress(data))