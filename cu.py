from database.session import SessionLocal
from database.models import User
from auth.security import get_password_hash

def criar_usuario():
    db = SessionLocal()
    try:
        # Verifica se o usuário já existe
        if db.query(User).filter(User.username == "dev").first():
            print("Usuário 'dev' já existe!")
            return

        # Cria o usuário
        usuario = User(
            id="1",
            username="dev",
            hashed_password=get_password_hash("senha123")
        )
        db.add(usuario)
        db.commit()
        print("Usuário criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    criar_usuario()