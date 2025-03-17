from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import config

# Configuração do banco de dados
engine = create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Permite uso em múltiplas threads
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()