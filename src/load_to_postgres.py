import os
import json
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Database connection
conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT')
)

cursor = conn.cursor()

# Create raw schema and table
cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        id BIGINT,
        channel VARCHAR,
        date TIMESTAMP,
        text TEXT,
        has_media BOOLEAN
    );
""")
conn.commit()

# Load JSON files
data_dir = '../data/raw/telegram_messages'
for root, _, files in os.walk(data_dir):
    for file in files:
        if file.endswith('messages.json'):
            channel = root.split('/')[-1]
            with open(os.path.join(root, file), 'r') as f:
                messages = json.load(f)
                for msg in messages:
                    cursor.execute("""
                        INSERT INTO raw.telegram_messages (id, channel, date, text, has_media)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (msg['id'], channel, msg['date'], msg['text'], msg['has_media']))
                conn.commit()

cursor.close()
conn.close()