from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# URL do banco de dados (ex.: postgresql://usuario:senha@localhost:5432/corretora_db)
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Base para os modelos do banco de dados
Base = declarative_base()

# Cria uma sessão local para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.models.user import User

Base.metadata.create_all(bind=engine)