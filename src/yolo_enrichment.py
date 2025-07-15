import os
import psycopg2
from ultralytics import YOLO
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

# Create table for detections
cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw.image_detections (
        message_id BIGINT,
        channel VARCHAR,
        detected_object_class VARCHAR,
        confidence_score FLOAT
    );
""")
conn.commit()

# Load YOLO model
model = YOLO('yolov8n.pt')

# Scan images
img_dir = '../data/raw/images'
for root, _, files in os.walk(img_dir):
    for file in files:
        if file.endswith('.jpg'):
            channel = root.split('/')[-1]
            message_id = int(file.split('.')[0])
            results = model(os.path.join(root, file))
            for result in results:
                for box in result.boxes:
                    cls = result.names[int(box.cls)]
                    conf = float(box.conf)
                    cursor.execute("""
                        INSERT INTO raw.image_detections (message_id, channel, detected_object_class, confidence_score)
                        VALUES (%s, %s, %s, %s)
                    """, (message_id, channel, cls, conf))
            conn.commit()

cursor.close()
conn.close()