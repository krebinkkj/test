from sqlalchemy import Column, String, LargeBinary
from database.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(255), primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)