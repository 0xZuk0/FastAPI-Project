import matplotlib
matplotlib.use('Agg')

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from psycopg2 import connect
from time import sleep
from .config import settings

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

# while True :
#     try :
#         conn = connect(host="localhost", database="fastapi", user="postgres", password="postgres", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("[+] Database connection Established...")
#         break
#     except Exception as error :
#         print(f"[!] Connecting to database failed!! - {error}")
#         sleep(2)