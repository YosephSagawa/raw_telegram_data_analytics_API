from pydantic import BaseModel
from typing import List

class TopProduct(BaseModel):
    product: str
    mention_count: int

class ChannelActivity(BaseModel):
    date: str
    message_count: int

class MessageSearch(BaseModel):
    message_id: int
    text: str
    channel_name: str