from airflow.decorators import dag, task
from datetime import datetime
from pathlib import Path
import pandas as pd

from src.validate import validate

RAW_DATA_DIR = Path("opt/airflow/data/raw")
PROCESSED_DIR = Path("opt/airflow/data/processed")

@dag(
    dag_id = "stock_etl_taskflow",
    start_date = datetime(2026, 1, 26),
    schedule_interval = None,
    catchup = False,
    tags = ["stocks", "test"],
)
def stock_etl_taskflow():

    @task
    def extract_files():
        from src.extract import extract_stock_data

        symbols = ["APPL", "MSFT", "GOOGL"]
        paths = []

        for symbol in symbols:
            path = extract_stock_data(symbol)
            paths.append(str(path))
        
        return paths
    
    @task
    def transform_data(file_paths: list[str]):
        from src.transform import transform

        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        processed_files = []

        for file_path in file_paths:
            df = pd.read_csv(file_path)
            df = transform(df)

            output_path = PROCESSED_DIR / Path(file_path).name
            df.to_csv(output_path, index=False)
            processed_files.append(str(output_path))

            print(f"Transformed: {output_path.name}")
        
        return processed_files
    
    @task
    def load_data(validated_files: list[str]):
        from src.load import load

        for file_path in validated_files:
            df = pd.read_csv(file_path)
            load(df)
            print(f"Loaded: {Path(file_path).name}")
    
    files = extract_files()
    transformed = transform_data(files)
    validated = validate(transformed)
    load_data(validated)
