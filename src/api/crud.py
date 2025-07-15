from sqlalchemy.orm import Session
from .models import Message
from sqlalchemy.sql import text

def get_top_products(db: Session, limit: int = 10):
    query = text("""
        SELECT
            REGEXP_SPLIT_TO_TABLE(text, E'\\s+') AS product,
            COUNT(*) AS mention_count
        FROM public_marts.fct_messages
        GROUP BY product
        ORDER BY mention_count DESC
        LIMIT :limit
    """)
    result = db.execute(query, {"limit": limit}).fetchall()
    return [{"product": row[0], "mention_count": row[1]} for row in result]

def get_channel_activity(db: Session, channel_name: str):
    query = text("""
        SELECT
            d.date,
            COUNT(*) AS message_count
        FROM public_marts.fct_messages m
        JOIN public_marts.dim_channels c ON m.channel_id = c.channel_id
        JOIN public_marts.dim_dates d ON m.date_id = d.date_id
        WHERE c.channel_name = :channel_name
        GROUP BY d.date
        ORDER BY d.date
    """)
    result = db.execute(query, {"channel_name": channel_name}).fetchall()
    return [{"date": str(row[0]), "message_count": row[1]} for row in result]

def search_messages(db: Session, query: str):
    query = text("""
        SELECT
            m.message_id,
            m.text,
            c.channel_name
        FROM public_marts.fct_messages m
        JOIN public_marts.dim_channels c ON m.channel_id = c.channel_id
        WHERE m.text ILIKE :query
    """)
    result = db.execute(query, {"query": f"%{query}%"}).fetchall()
    return [{"message_id": row[0], "text": row[1], "channel_name": row[2]} for row in result]