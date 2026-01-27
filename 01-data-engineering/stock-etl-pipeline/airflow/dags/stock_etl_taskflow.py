from airflow.decorators import dag, task
from datetime import datetime
from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path("/opt/airflow/data/raw")
PROCESSED_DIR = Path("/opt/airflow/data/processed")

@dag(
    dag_id = "stock_etl_taskflow",
    start_date = datetime(2026, 1, 26),
    schedule_interval = None,
    catchup = False,
    tags = ["stocks", "test"],
)
def stock_etl_taskflow():

    # 🔹 Creation of table on PostgreSQL if not exists
    @task
    def init_db():
        from src.db import get_connection

        sql = """
        CREATE TABLE IF NOT EXISTS stocks(
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
        """

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        print("✅ Table stocks prête")

    @task
    def extract_files():
        from src.extract import extract_stock_data
        import logging

        symbols = ["AAPL", "MSFT", "GOOGL"]
        paths = []

        for symbol in symbols:
            path = extract_stock_data(symbol)
            paths.append(str(path))
        
        logging.info(f"✅ il y a {len(paths)} fichiers CSV extraits")
        return paths
    
    @task
    def transform_data(file_paths: list[str]):
        from src.transform import transform

        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        processed_files = []

        for file_path in file_paths:
            df = pd.read_csv(file_path, sep=",", header=0, encoding="utf-8")
            df = transform(df)

            output_path = PROCESSED_DIR / Path(file_path).name
            df.to_csv(output_path, index=False)
            processed_files.append(str(output_path))

            print(f"Transformed: {output_path.name}")
        
        return processed_files
    
    @task
    def validate_data(processed_files: list[str]):
        from src.validate import validate

        for file_path in processed_files:
            df = pd.read_csv(file_path, parse_dates=['date'])
            validate(df)
            print(f"Validated: {Path(file_path).name}")
        return processed_files

    
    @task
    def load_data(validated_files: list[str]):
        from src.load import load

        for file_path in validated_files:
            df = pd.read_csv(file_path)
            load(df)
            print(f"Loaded: {Path(file_path).name}")
    
    init = init_db()
    files = extract_files()
    transformed = transform_data(files)
    validated = validate_data(transformed)
    load_data(validated)

    init >> files

stock_etl_taskflow()