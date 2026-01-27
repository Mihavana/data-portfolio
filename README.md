# Data Portfolio

This repository contains my projects related to data engineering, data analysis, and machine learning. The goal is to showcase my practical skills in data management, ETL pipeline creation, analysis and ML modeling, and model deployment.

## 📁 Repository Structure
```
data-portfolio/
├── 01-data-engineering-pipeline/   # ETL & Data Engineering projects
│   └── stock-etl-pipeline/         # ETL pipeline for stock market data
├── 02-data-analysis-dashboard/     # (Coming soon) Dashboard and data analysis
├── 03-machine-learning-project/    # (Coming soon) Machine Learning & modeling projects
├── 04-ml-api-deployment/           # (Coming soon) ML API deployment
└── README.md                       # This file
```

## 🛠 Technologies Used

- **Python**: ETL scripting, data analysis, machine learning
- **pandas / numpy / scikit-learn**: data manipulation and modeling
- **PostgreSQL**: data storage and management
- **Airflow**: ETL pipeline orchestration and scheduling
- **Docker / Docker Compose**: pipeline and service containerization
- **Flask / FastAPI**: for ML API deployment (planned in 04-ml-api-deployment)
- **Power BI / Plotly**: visualization and dashboards (planned in 02-data-analysis-dashboard)

## 🚀 Completed Projects

### 01 - Data Engineering Pipeline

- **Objective**: Build an ETL pipeline for stock market data
- **Features**:
  - Data extraction from CSV files
  - Data transformation and cleaning
  - Data validation
  - Loading into PostgreSQL
  - Orchestration with Airflow
  - Detailed logging for each step
- **Structure**:
```
stock-etl-pipeline/
├── docker/
│   ├── docker-compose.yml              # Main PostgreSQL database
│   ├── docker-compose-airflow.yml      # Airflow services (webserver, scheduler)
│   └── Dockerfile.airflow              # Custom Airflow image with dependencies
│
├── airflow/
│   └── dags/
│       ├── stock_etl_main.py           # DAG calling the src : transform, load
│       └── stock_etl_simple.py         # Simplified DAG for development
│
├── src/
│   ├── create_table.py                 # Database table creation
│   ├── db.py                           # Database connection setup
│   ├── extract.py                      # Data extraction (Yahoo Finance API)
│   ├── transform.py                    # Data cleaning and transformation
│   ├── validate.py                     # Data quality checks
│   ├── load.py                         # Data loading into PostgreSQL
│   └── main.py                         # Main script (can be run standalone)
│
├── data/
│   └── raw/                            # Raw CSV data storage
│
├── logs/                               # Pipeline execution logs
│
├── requirements.txt                    # Python dependencies
└── README.md
```

## 💡 Best Practices

- All projects are containerized via Docker to ensure reproducibility
- Logs and raw data are separated to facilitate debugging and re-execution
- Airflow DAGs use relative paths and Docker volumes to access scripts and data