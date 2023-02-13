import os
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
import pendulum

with DAG(
    'phishing_domain_detection_batch_prediction',
    default_args={'retries': 2},
    description='Phishing Domain Detection',
    schedule_interval='@weekly',
    start_date=pendulum.datetime(2022, 2, 5, tz='UTC'),
    catchup=False,
) as dag:
    def prediction(**kwargs):
        from phishing.pipeline.batch_pipeline import batch_prediction
        input_dir = '/app/input_files'
        for files in os.listdir(input_dir):
            batch_prediction(input_file_path=os.path.join(input_dir, files))
        
    def download_file(**kwargs):
        bucket_name=os.getenv('BUCKET_NAME')
        input_dir = '/app/input_files'
        os.makedirs(input_dir, exist_ok=True)
        os.system(f'aws s3 sync s3://{bucket_name}/input_files /app/input_files')

    def sync_with_s3_bucket(**kwargs):
        bucket_name=os.getenv('BUCKET_NAME')
        os.system(f'aws s3 sync /app/Prediction s3://{bucket_name}/prediction')

    batch_prediction = PythonOperator(
        task_id='batch_prediction',
        python_callable=prediction
    )

    download_files = PythonOperator(
        task_id='dowload_files_from_s3',
        python_callable=download_file
    )

    sync_data_with_s3 = PythonOperator(
        task_id='sync_data_with_s3',
        python_callable=sync_with_s3_bucket
    )

    download_files >> batch_prediction >> sync_data_with_s3
