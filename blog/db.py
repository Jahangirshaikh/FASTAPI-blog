from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


sqlite_url = "sqlite:///./blog.db"

engine = create_engine(sqlite_url, connect_args={"check_same_thread":False})

Base = declarative_base()

SessionLocal = sessionmaker(autoflush=False, bind=engine)




