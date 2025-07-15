from dagster import job, op, schedule, repository
import subprocess
import os

@op
def scrape_telegram_data():
    subprocess.run(["python", "src/scrape_telegram.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "src/load_to_postgres.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "dbt_project"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "src/yolo_enrichment.py"], check=True)

@job
def medical_data_pipeline():
    load_raw_to_postgres(scrape_telegram_data())
    run_dbt_transformations(load_raw_to_postgres())
    run_yolo_enrichment(run_dbt_transformations())

@schedule(cron_schedule="0 0 * * *", job=medical_data_pipeline)
def daily_medical_pipeline():
    return {}

@repository
def medical_data_repository():
    return [medical_data_pipeline, daily_medical_pipeline]