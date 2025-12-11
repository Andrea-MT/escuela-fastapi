from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "escuela")
ENCODED_PASSWORD = quote(DB_PASSWORD, safe='')

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{ENCODED_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    print(f"URL: {SQLALCHEMY_DATABASE_URL}")
    print("Asegúrate de que la URL de RDS es correcta en el archivo .env")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()