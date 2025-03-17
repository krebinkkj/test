import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "teste")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ai_database.db")  # Arquivo .db
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    JWT_ALGORITHM = "HS512"
    JWT_EXPIRE_MINUTES = 300

config = Config()