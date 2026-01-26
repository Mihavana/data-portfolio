<h1 align="center">📈 Stock ETL Pipeline</h1>
<p align="center">
  ETL pipeline in Python for financial data (PostgreSQL)
</p>

---

## 🎯 Project Objective
This project demonstrates the implementation of an **ETL pipeline (Extract, Transform, Load)** to:
- collect financial stock data,
- clean and structure it,
- then load it into a **PostgreSQL** database.

The goal is to showcase **Data Engineering best practices** applicable in a professional environment: modularity, idempotence, error handling, and code clarity.

---

## 🏗️ Project Structure

```text
data-engineering/
└── stock-etl-pipeline/
    ├── docker-compose.yml      # Docker Compose file to run PostgreSQL
    ├── src/
    │   ├── create_table.py     # Database table creation
    │   ├── db.py               # Database connection setup
    │   ├── extract.py          # Data extraction (API / CSV files)
    │   ├── transform.py        # Data cleaning and transformation
    │   ├── validate.py         # Data quality checks
    │   ├── load.py             # Data loading into PostgreSQL
    │   └── main.py             # Main script to run the full pipeline
    │
    ├── data/
    │   └── raw/                # Raw CSV data
    │
    ├── logs/                   # Logs of pipeline execution
    │
    ├── requirements.txt        # Python dependencies
    └── README.md
```
## 🔄 Pipeline Workflow

### 1. Extract
* Fetch stock data (via CSV or API)
* Add metadata:
   * `symbol` (stock ticker)
   * `extracted_at` (timestamp of extraction)

### 2. Transform
* Parse dates and handle timezones
* Convert columns to appropriate types (`float`, `int`, `datetime`)
* Normalize column names
* Handle invalid or missing values

### 3. Load
* Insert data into PostgreSQL
* Maintain idempotence to avoid duplicates
* Ensure safe reloads in case the pipeline is rerun

## 🔐 Idempotence

The pipeline can be safely rerun multiple times without creating duplicates thanks to:

* A `UNIQUE (symbol, date)` constraint in PostgreSQL
* The use of `ON CONFLICT DO NOTHING` in the insert statements

This ensures data integrity and allows for safe reruns of the pipeline without worrying about duplicate entries.

## 🧰 Technologies Used

* **Python 3** - Core programming language
* **Pandas** - Data manipulation and analysis
* **PostgreSQL** - Relational database for data storage
* **psycopg2** - PostgreSQL adapter for Python
* **Docker / Docker Compose** - Containerized PostgreSQL deployment
* **Git / GitHub** - Version control

## 🚀 Running the Pipeline

### Prerequisites

- Docker and Docker Compose installed
- Python 3.x installed
- Required Python packages (see Installation section)

### 1. Start PostgreSQL using Docker Compose

```bash
docker-compose up -d
```

This will start the PostgreSQL container in the background.

### 2. Create the database table (first time only)

```bash
python src/create_table.py
```

This script creates the necessary table structure with the appropriate constraints and indexes.

### 3. Run the ETL pipeline

```bash
python src/main.py
```