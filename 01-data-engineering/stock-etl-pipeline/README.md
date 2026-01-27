<h1 align="center">📈 Stock ETL Pipeline</h1>
<p align="center">
  Automated ETL pipeline with Airflow for financial data orchestration
</p>

---

## 🎯 Project Objective

This project demonstrates the implementation of a **production-ready ETL pipeline** orchestrated with **Apache Airflow** to:
- Extract financial stock data from Yahoo Finance API
- Clean, validate, and transform the data
- Load it into a **PostgreSQL** database
- Automate the entire workflow with scheduled executions

The goal is to showcase **Data Engineering best practices** applicable in a professional environment: modularity, orchestration, idempotence, error handling, containerization, and monitoring.

---

## 🏗️ Project Structure

```text
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
│
├── requirements.txt                    # Python dependencies
└── README.md
```

---

## 🔄 Pipeline Workflow

### 1. **Extract**
- Fetch stock data from Yahoo Finance API using `yfinance`
- Support for multiple stock symbols (AAPL, GOOGL, MSFT, etc.)
- Add metadata:
  - `symbol` (stock ticker)
  - `extracted_at` (timestamp of extraction)
- Store raw data as CSV files

### 2. **Transform**
- Parse dates and handle timezones
- Convert columns to appropriate types (`float`, `int`, `datetime`)
- Normalize column names (lowercase, underscore format)
- Handle invalid or missing values
- Remove duplicates based on `(symbol, date)` pairs
- Validate data quality (non-negative prices, valid volumes)

### 3. **Load**
- Insert cleaned data into PostgreSQL
- Maintain idempotence with `ON CONFLICT DO NOTHING`
- Handle large datasets efficiently with row-by-row insertion
- Track inserted vs. skipped (duplicate) rows

### 4. **Orchestration**
- Automated scheduling with Apache Airflow
- Daily execution at configurable times
- Comprehensive logging and monitoring
- Error handling and retry mechanisms
- Web UI for pipeline visualization and management

---

## 🔐 Idempotence & Data Integrity

The pipeline ensures data integrity through:
- **UNIQUE constraint** on `(symbol, date)` in PostgreSQL
- **ON CONFLICT DO NOTHING** in INSERT statements
- Safe reruns without creating duplicates
- Automatic tracking of inserted vs. skipped rows

This design allows the pipeline to be safely rerun multiple times, making it resilient to failures and suitable for production environments.

---

## 🧰 Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Apache Airflow 2.7.1** | Workflow orchestration & scheduling |
| **Pandas** | Data manipulation and analysis |
| **PostgreSQL 13** | Relational database for data storage |
| **psycopg2-binary** | PostgreSQL adapter for Python |
| **yfinance** | Yahoo Finance API client |
| **Docker & Docker Compose** | Containerized deployment |
| **Git / GitHub** | Version control |

---

## 🚀 Getting Started

### Prerequisites

- **Docker** and **Docker Compose** installed
- **Python 3.8+** installed (for local development)
- At least **4GB RAM** for Airflow containers
- Basic understanding of SQL and data pipelines

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Mihavana/data-portfolio.git
cd stock-etl-pipeline
```

### 2. Start PostgreSQL Database

```bash
cd docker
docker-compose up -d
```

This starts the PostgreSQL container on port **5432**.

**Verify it's running:**
```bash
docker ps | grep postgres
```

### 3. Create the Database Table

```bash
# From the project root
python src/create_table.py
```

This creates the `stocks` table with the following schema:

```sql
CREATE TABLE IF NOT EXISTS stocks (
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    dividends NUMERIC,
    stock_splits NUMERIC,
    extracted_at TIMESTAMP NOT NULL,
    PRIMARY KEY (symbol, date)
);
```

### 4. Build and Start Airflow

```bash
cd docker

# Build custom Airflow image with dependencies
docker-compose -f docker-compose-airflow.yml build --no-cache

# Start Airflow services
docker-compose -f docker-compose-airflow.yml up -d
```

This starts:
- **Airflow Webserver** on port **8080**
- **Airflow Scheduler** (background process)
- **Airflow Metadata Database** on port **5433**

**Wait ~30 seconds** for services to initialize.

### 5. Initialize Airflow (First Time Only)

```bash
# Initialize Airflow database
docker exec airflow-scheduler airflow db init

# Create admin user
docker exec airflow-scheduler airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Restart webserver to apply changes
docker-compose -f docker-compose-airflow.yml restart airflow-webserver
```

### 6. Access Airflow Web UI

Open your browser and navigate to:

```
http://localhost:8080
```

**Login credentials:**
- Username: `admin`
- Password: `admin`

---

## 🎮 Using the Pipeline

### Option A: Run via Airflow (Recommended)

1. **Access the Airflow UI** at `http://localhost:8080`

2. **Find the DAG** named `stock_etl_simple` in the list

3. **Enable the DAG** by toggling the switch on the left

4. **Trigger manually** by clicking the ▶️ (play) button

5. **Monitor execution:**
   - Click on the DAG name
   - Select **Graph** tab to see visual workflow
   - Click on the task box → **Log** button to view detailed logs

6. **View results:**
   ```bash
   # Check loaded data
   docker exec postgres psql -U user -d portfolio_db -c \
     "SELECT symbol, COUNT(*) FROM stocks GROUP BY symbol;"
   ```

   Expected output:
   ```
    symbol | count 
   --------+-------
    AAPL   |  1018
    GOOGL  |  1018
    MSFT   |  1018
   ```

### Option B: Run Standalone (Development)

```bash
# Extract data
python src/extract.py

# Transform data
python src/transform.py

# Load to database
python src/load.py

# Or run the full pipeline
python src/main.py
```

---

## 📊 Monitoring & Logs

### Airflow Web UI

- **DAGs Overview**: `http://localhost:8080`
- **Task Logs**: Click on task → Log button
- **Execution History**: Grid view shows all past runs
- **Task Duration**: Graph view displays execution times

### Container Logs

```bash
# Airflow scheduler logs
docker logs airflow-scheduler

# Airflow webserver logs
docker logs airflow-webserver

# PostgreSQL logs
docker logs postgres
```

### Application Logs

```bash
# View logs directory
ls -lh logs/

# Read specific log file
cat logs/pipeline_2024-01-26.log
```

---

## 🔧 Configuration

### Database Connection

Edit `src/db.py` to modify database settings:

```python
db_config = {
    'host': 'portfolio_postgres_db',           # Container name in Docker network
    'port': 5432,
    'database': 'portfolio_db',
    'user': 'user',
    'password': 'password'
}
```

### Stock Symbols

Edit `src/extract.py` to add/remove stock symbols:

```python
STOCK_SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
```

### Schedule Interval

Edit `airflow/dags/stock_etl_simple.py`:

```python
with DAG(
    dag_id='stock_etl_simple',
    start_date=datetime(2026, 1, 26),
    schedule_interval='0 0 * * *',  # Run daily at midnight
    catchup=False,
) as dag:
```

Schedule formats:
- `'0 0 * * *'` - Daily at midnight
- `'0 */6 * * *'` - Every 6 hours
- `'0 9 * * 1-5'` - Weekdays at 9 AM
- `None` - Manual trigger only

---

## 🐛 Troubleshooting

### Issue: Airflow UI not accessible

**Solution:**
```bash
# Check if containers are running
docker ps

# Restart webserver
docker-compose -f docker-compose-airflow.yml restart airflow-webserver

# Check logs for errors
docker logs airflow-webserver
```

### Issue: "Connection refused" to database

**Solution:**
- Ensure you're using `'host': 'postgres'` (not `'localhost'`)
- Verify containers are on the same network:
  ```bash
  docker network ls
  docker inspect airflow-scheduler | grep NetworkMode
  ```

### Issue: "Table does not exist"

**Solution:**
```bash
# Recreate the table
python src/create_table.py

# Verify it exists
docker exec postgres psql -U user -d portfolio_db -c "\d stocks"
```

### Issue: DAG not appearing in Airflow

**Solution:**
```bash
# Copy DAG to Airflow
docker cp airflow/dags/stock_etl_simple.py airflow-scheduler:/opt/airflow/dags/

# Restart scheduler
docker-compose -f docker-compose-airflow.yml restart airflow-scheduler
```

---

## 🧪 Testing

### Test Database Connection

```bash
docker exec postgres psql -U user -d portfolio_db -c "SELECT version();"
```

### Test Data Extraction

```bash
python src/extract.py
ls -lh data/raw/
```

### Test Full Pipeline (Standalone)

```bash
python src/main.py
```

Expected output:
```
Pipeline completed: 3 succeeded, 0 failed
Total rows loaded: 3054
```

---
