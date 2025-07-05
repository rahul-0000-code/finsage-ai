from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    filename = Column(String)
    file_url = Column(String)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
