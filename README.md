# ETL Data Pipeline with Apache Airflow

## Project Overview
This project demonstrates the design and implementation of a **modular ETL (Extract, Transform, Load) pipeline** using **Apache Airflow**. The pipeline automates the process of collecting data from an external API, transforming it into a clean and structured format, and loading it into a target database for further analysis.  

The goal is to build a **reusable and scalable data pipeline** that reflects industry practices in Data Engineering.

---

## Key Features
- **Orchestrated Workflow**: Tasks are scheduled and executed in sequence using Apache Airflow DAGs.  
- **Data Extraction**: API requests are automated using Airflow operators.  
- **Data Transformation**: Raw data is cleaned and transformed into meaningful tables.  
- **Data Loading**: Transformed data is inserted into a Postgres database for storage and querying.  
- **Error Handling & Logging**: Built-in Airflow monitoring ensures transparency and reliability.  
- **Reusability**: The pipeline can be adapted for different datasets or APIs with minimal changes.  

---

## Tech Stack
- **Apache Airflow** – Workflow orchestration  
- **PostgreSQL** – Data storage  
- **Python** – Transformation logic  
- **Astro CLI** – Local Airflow development environment  
- **Docker** – Containerized execution  





