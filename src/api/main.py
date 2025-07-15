from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .database import SessionLocal
from .crud import get_top_products, get_channel_activity, search_messages
from .schemas import TopProduct, ChannelActivity, MessageSearch
from typing import List
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.get("/api/reports/top-products", response_model=List[TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return get_top_products(db, limit)

@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    return get_channel_activity(db, channel_name)

@app.get("/api/search/messages", response_model=List[MessageSearch])
def search_messages_endpoint(query: str, db: Session = Depends(get_db)):
    return search_messages(db, query)