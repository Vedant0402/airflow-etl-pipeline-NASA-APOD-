from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import json

# Define the DAG
with DAG(
    dag_id='nasa_apod_postgres',
    start_date=datetime(2025, 8, 15),
    schedule='@daily',
    catchup=False
) as dag:

    # Step 1: Create table
    @task
    def create_table():
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        postgres_hook.run(create_table_query)

    # Step 2: Extract NASA APOD Data
    extract_apod = HttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',
        endpoint='planetary/apod?api_key={{ conn.nasa_api.extra_dejson.api_key }}',
        method='GET',
        response_filter=lambda response: response.json(),
        log_response=True
    )

    # Step 3: Transform
    @task
    def transform_apod_data(response):
        apod_data = {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),  # already YYYY-MM-DD format
            'media_type': response.get('media_type', '')
        }
        return apod_data

    # Step 4: Load into Postgres
    @task
    def load_data_to_postgres(apod_data: dict):
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """
        postgres_hook.run(insert_query, parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))

    # Step 5: Set dependencies
    create_table_task = create_table()
    transformed_data = transform_apod_data(extract_apod.output)
    load_task = load_data_to_postgres(transformed_data)

    create_table_task >> extract_apod >> transformed_data >> load_task


    