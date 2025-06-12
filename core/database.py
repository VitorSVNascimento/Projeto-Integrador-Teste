from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
#Criação da base que será utilizada para os modelos
Base = declarative_base()
# Configurações da conexão com o PostgreSQL
usuario = 'postgres'
senha = '12345678'
host = 'localhost' # ou o IP do servidor, caso não seja local
banco = 'testeprojeto'
# String de conexão
DATABASE_URL = os.getenv('BD_CONNECTION_STRING')
# Cria a engine que faz a conexão com o banco
engine = create_engine(DATABASE_URL)
# Cria uma fábrica de sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
