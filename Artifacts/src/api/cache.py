"""
Redis caching layer for predictions
"""

import json
import hashlib
import logging
from typing import Optional, Any
from datetime import datetime, timedelta

from .config import settings

logger = logging.getLogger(__name__)

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available. Install with: pip install redis")


class Cache:
    """Redis cache manager"""
    
    def __init__(self):
        self.client = None
        self.enabled = settings.model_cache_enabled and REDIS_AVAILABLE
        
        if self.enabled:
            try:
                self.client = redis.Redis(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    password=settings.redis_password if settings.redis_password else None,
                    db=settings.redis_db,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )
                # Test connection
                self.client.ping()
                logger.info("Redis cache connected successfully")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}. Caching disabled.")
                self.enabled = False
                self.client = None
        else:
            logger.info("Redis cache disabled or not available")
    
    def _generate_key(self, data: dict) -> str:
        """Generate cache key from transaction data"""
        # Create hash of sorted transaction features
        data_str = json.dumps(data, sort_keys=True)
        key_hash = hashlib.md5(data_str.encode()).hexdigest()
        return f"guardian:prediction:{key_hash}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled or not self.client:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with TTL"""
        if not self.enabled or not self.client:
            return False
        
        try:
            ttl = ttl or settings.redis_ttl
            self.client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
            return True
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    def get_prediction(self, transaction_data: dict) -> Optional[dict]:
        """Get cached prediction for transaction"""
        if not self.enabled:
            return None
        
        key = self._generate_key(transaction_data)
        return self.get(key)
    
    def set_prediction(self, transaction_data: dict, prediction: dict, ttl: Optional[int] = None) -> bool:
        """Cache prediction for transaction"""
        if not self.enabled:
            return False
        
        key = self._generate_key(transaction_data)
        return self.set(key, prediction, ttl)
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.enabled or not self.client:
            return False
        
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    def clear(self, pattern: str = "guardian:*") -> int:
        """Clear cache entries matching pattern"""
        if not self.enabled or not self.client:
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        if not self.enabled or not self.client:
            return False
        
        try:
            self.client.ping()
            return True
        except Exception:
            return False


# Global cache instance
cache = Cache()

