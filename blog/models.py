from sqlalchemy import Column, Integer, String
from .db import Base

class Blog(Base):
    __tablename__ = "Blog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String[50])
    body = Column(String) 


