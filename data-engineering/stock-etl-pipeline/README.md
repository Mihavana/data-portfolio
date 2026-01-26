<h1 align="center">Stock ETL Pipeline</h1>

## Project Objective
This project demonstrates the implementation of an **ETL pipeline (Extract, Transform, Load)** to:
- collect financial stock data,
- clean and structure it,
- then load it into a **PostgreSQL** database.

The goal is to showcase **Data Engineering best practices** applicable in a professional environment: modularity, idempotence, error handling, and code clarity.

---

## Project Structure

```text
data-engineering/
└── stock-etl-pipeline/
    ├── src/
    │   ├── create_table.py     # Database table creation
    │   ├── db.py               # Database connection setup
    │   ├── extract.py          # Data extraction (API / CSV files)
    │   ├── transform.py        # Data cleaning and transformation
    │   ├── load.py             # Data loading into PostgreSQL
    │   └── main.py             # Main script to run the full pipeline
    │
    ├── data/
    │   └── raw/                # Raw CSV data
    │
    ├── requirements.txt        # Python dependencies
    └── README.md