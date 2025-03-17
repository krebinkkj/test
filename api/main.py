from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.session import get_db
from auth.security import (
    get_password_hash,
    username_exists,
    create_access_token,
    get_current_user,
    authenticate_user
)
from database.models import User
from core.ai import CodeAssistant
import uuid

app = FastAPI()

# Modelo para o corpo da requisição de registro
class RegisterRequest(BaseModel):
    username: str
    password: str

# Modelo para o corpo da requisição de análise
class AnalysisRequest(BaseModel):
    code: str

@app.post("/register")
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    # Verifica se o nome de usuário já existe
    if username_exists(db, request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já está em uso."
        )

    # Cria o usuário
    try:
        user = User(
            id=str(uuid.uuid4()),  # Gera um ID único
            username=request.username,
            hashed_password=get_password_hash(request.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

    return {
        "status": "success",
        "message": "Usuário registrado com sucesso!"
    }

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Credenciais inválidas"
        )
    return {
        "access_token": create_access_token({"sub": user.username}),
        "token_type": "bearer"
    }

@app.post("/analyze")
async def analyze_code(
    request: AnalysisRequest,
    user: User = Depends(get_current_user)
):
    try:
        assistant = CodeAssistant()
        result = assistant.process(request.code)
        return {
            "user": user.username,
            "analysis": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))