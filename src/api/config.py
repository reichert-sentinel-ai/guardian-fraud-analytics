"""
Configuration settings for Guardian API
"""

import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    api_title: str = "Guardian Fraud Detection API"
    api_description: str = "Real-time fraud detection and explainability API"
    api_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Server Settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # CORS Settings
    cors_enabled: bool = True
    cors_origins: List[str] = ["*"]  # Configure for production
    
    # Database Settings (PostgreSQL)
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_user: str = os.getenv("DB_USER", "guardian")
    db_password: str = os.getenv("DB_PASSWORD", "guardian")
    db_name: str = os.getenv("DB_NAME", "guardian_db")
    
    @property
    def database_url(self) -> str:
        """Build PostgreSQL database URL"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    # Redis Settings
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    redis_ttl: int = int(os.getenv("REDIS_TTL", "3600"))  # 1 hour default
    
    @property
    def redis_url(self) -> str:
        """Build Redis URL"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    # Model Settings
    model_path: str = os.getenv("MODEL_PATH", "models/xgboost_fraud_latest.pkl")
    model_cache_enabled: bool = True
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

