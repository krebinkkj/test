from database.session import Base, engine

def init_db():
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print(f"Tabelas criadas com sucesso! Banco de dados: {engine.url}")

if __name__ == "__main__":
    init_db()