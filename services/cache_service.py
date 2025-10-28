"""
Redis Caching Service for Feature Extraction
Provides caching layer to avoid redundant computations
"""

import logging
import hashlib
import pickle
from typing import Optional, List
import redis
from config import config
import os

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis-based caching for feature vectors and results"""
    
    def __init__(self):
        """Initialize Redis connection"""
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))
        
        try:
            self.redis = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                decode_responses=False,
                socket_connect_timeout=5
            )
            self.redis.ping()
            logger.info(f" Redis cache connected: {redis_host}:{redis_port}")
        except Exception as e:
            logger.warning(f" Redis not available: {e}. Continuing without cache.")
            self.redis = None
    
    def _generate_key(self, prefix: str, data: bytes) -> str:
        """Generate cache key from image data"""
        hash_digest = hashlib.md5(data).hexdigest()
        return f"{prefix}:{hash_digest}"
    
    def get_features(self, image_bytes: bytes) -> Optional[List[float]]:
        """Get cached features for image"""
        if not self.redis:
            return None
        
        try:
            cache_key = self._generate_key("features", image_bytes)
            cached = self.redis.get(cache_key)
            
            if cached:
                logger.info(f" Cache HIT: {cache_key[:20]}...")
                return pickle.loads(cached)
            
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set_features(self, image_bytes: bytes, features: List[float], ttl: int = 86400) -> bool:
        """Cache features with TTL"""
        if not self.redis:
            return False
        
        try:
            cache_key = self._generate_key("features", image_bytes)
            self.redis.setex(cache_key, ttl, pickle.dumps(features))
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        if not self.redis:
            return {
                "status": "disconnected",
                "total_keys": 0,
                "memory_used": "N/A"
            }
        
        try:
            info = self.redis.info()
            return {
                "status": "connected",
                "total_keys": self.redis.dbsize(),
                "memory_used": f"{info.get('used_memory_human', 'N/A')}",
                "connected_clients": info.get('connected_clients', 0)
            }
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }


_cache_instance = None


def get_cache():
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache()
    return _cache_instance
