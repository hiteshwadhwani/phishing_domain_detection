import os
from airfow import DAG
from airflow.operators.python import PythonOperator
import json
import pendulum

with DAG(
    'phishing_domain_detection_training',
    default_args={'retries': 2},
    description='Phishing Domain Detection',
    schedule_interval='@weekly',
    start_date=pendulum.datetime(2023, 2, 5, tz='UTC'),
    catchup=False,
) as dag:
    def training(**kwargs):
        from phishing.pipeline.training_pipeline import start_training_pipeline
        start_training_pipeline()

    def sync_data_to_s3():
        bucket_name = os.getenv('BUCKET_NAME')
        os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts")
        os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/saved_models")

    training_pipeline = PythonOperator(
        task_id='training_pipeline',
        python_callable=training
    )

    sync_to_s3 = PythonOperator(
        task_id='sync_data_to_s3',
        python_callable=sync_data_to_s3
    )

    training_pipeline >> sync_to_s3
    