## Medical Data Pipeline

This project implements a data pipeline for Kara Solutions to collect, process, and analyze medical-related data from Telegram channels. It scrapes messages and images from channels like chemed123, lobelia4cosmetics, and tikvahpharma, stores raw data in a local data lake, loads it into a PostgreSQL database, transforms it into a star schema using dbt, enriches images with YOLOv8 object detection, exposes analytical endpoints via a FastAPI application, and orchestrates the pipeline with Dagster.

## Project Overview

The pipeline performs the following tasks:

Data Scraping: Uses Telethon to scrape messages and images from Telegram channels, storing them as JSON and image files in a partitioned data lake.
Data Loading: Loads JSON data into a PostgreSQL database (medical_db) using psycopg2.
Data Transformation: Uses dbt to transform raw data into a star schema with staging views and mart tables (dim_channels, dim_dates, fct_messages, fct_image_detections).
Data Enrichment: Applies YOLOv8 to detect objects in images and stores results in the database.
Analytical API: Exposes endpoints via FastAPI for querying top products, channel activity, and message search.
Orchestration: Uses Dagster to schedule and manage the pipeline.

## Setup Instructions

Clone the Repository
git clone https://github.com/YosephSagawa/raw_telegram_data_analytics_API.git
cd raw_telegram_data_analytics_API

Set Up PostgreSQL

Install PostgreSQL from postgresql.org.
Start the PostgreSQL service:
Open services.msc, find postgresql-x64-15, and ensure it’s running.

In pgAdmin:
Create database medical_db:
Right-click Databases → Create → Database → Name: medical_db → Save.

Create user kara_user:
Right-click Login/Group Roles → Create → Login/Group Role → Name: kara_user, Password: kara_pass, Check Can login? → Save.

Grant privileges:
Right-click medical_db → Properties → Privileges → Add kara_user, Check ALL (or CREATE, CONNECT) → Save.
Right-click Schemas → public → Properties → Privileges → Add kara_user, Check USAGE, CREATE → Save.

Create Virtual Environment
python -m venv venv
.\venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Configure Environment Variables

Create .env in the project root:TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=your_phone_number
POSTGRES_USER=kara_user
POSTGRES_PASSWORD=kara_pass
POSTGRES_DB=medical_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

Replace your_api_id, your_api_hash, and your_phone_number with your Telegram API credentials.

Configure dbt

Create C:\Users\<YourUsername>\.dbt\profiles.yml:medical_data_pipeline:
target: dev
outputs:
dev:
type: postgres
host: localhost
user: kara_user
password: kara_pass
port: 5432
dbname: medical_db
schema: public

Ensure dbt_project.yml in dbt-project/ has profile: 'medical_data_pipeline'.

Create Project Directories
mkdir -p data/raw/telegram_messages data/raw/images logs dbt-project/models/staging dbt-project/models/marts dbt-project/tests src/api

Project Structure
raw_telegram_data_analytics_API/
├── .env # Environment variables
├── .gitignore # Git ignore file
├── requirements.txt # Python dependencies
├── src/ # Python scripts
│ ├── scrape_telegram.py # Scrapes Telegram data
│ ├── load_to_postgres.py # Loads data to PostgreSQL
│ ├── yolo_enrichment.py # Enriches images with YOLOv8
│ ├── api/ # FastAPI application
│ │ ├── main.py
│ │ ├── database.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ └── crud.py
│ └── pipeline.py # Dagster pipeline
├── dbt-project/ # dbt project
│ ├── dbt_project.yml
│ ├── models/
│ │ ├── staging/
│ │ │ └── stg_telegram_messages.sql
│ │ └── marts/
│ │ ├── dim_channels.sql
│ │ ├── dim_dates.sql
│ │ ├── fct_messages.sql
│ │ └── fct_image_detections.sql
│ └── tests/
│ └── unique_message_id.sql
├── data/ # Data lake
│ └── raw/
│ ├── telegram_messages/
│ └── images/
└── logs/ # Log files
└── scrape.log

Usage

Scrape Telegram Data
cd src
python .\scrape_telegram.py

Outputs JSON files to data/raw/telegram_messages/YYYY-MM-DD/channel_name/ and images to data/raw/images/YYYY-MM-DD/channel_name/.
Check logs/scrape.log for details.

Load Data to PostgreSQL
python .\load_to_postgres.py

Loads JSON data into raw.telegram_messages in medical_db.
Verify in pgAdmin: Schemas → raw → Tables → telegram_messages → View/Edit Data.

Run dbt Transformations
cd ..\dbt-project
dbt run
dbt test
dbt docs generate
dbt docs serve

Creates staging views (staging.stg_telegram_messages) and mart tables (marts.dim_channels, marts.dim_dates, marts.fct_messages).
Access documentation at http://localhost:8080.

Enrich Images with YOLOv8
cd ..\src
python .\yolo_enrichment.py

Processes images and loads detections into raw.image_detections.
Run dbt run again to create marts.fct_image_detections.

Start FastAPI Server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

Endpoints:
GET /api/reports/top-products: Top 10 mentioned products.
GET /api/channels/{channel_name}/activity: Channel posting activity.
GET /api/search/messages?query={keyword}: Search messages.

Test: curl http://localhost:8000/api/reports/top-products or visit http://localhost:8000/docs.

Run Dagster Pipeline
cd ..
dagster dev

Access UI at http://localhost:3000 to trigger or monitor the pipeline.
Scheduled to run daily at midnight.
