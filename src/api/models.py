from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from .database import Base

class Message(Base):
    __tablename__ = "marts.fct_messages"
    message_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer)
    date_id = Column(Integer)
    text = Column(String)
    has_media = Column(Boolean)
    message_length = Column(Integer)