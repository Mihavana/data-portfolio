# src/main.py
import pandas as pd
from pathlib import Path
import logging
import os

# Imports relatifs corrects pour un package
from src.transform import transform
from src.load import load
from src.validate import validate

def get_raw_data_dir():
    """
    Determine the correct raw data path depending on environment.
    - If running inside Airflow, use /opt/airflow/data/raw
    - Else, assume local execution relative path
    """
    if os.environ.get("AIRFLOW_CTX_DAG_ID"):  # Airflow sets this variable for DAG runs
        return Path("/opt/airflow/data/raw")
    else:
        # Chemin relatif depuis la racine du projet
        return Path(__file__).parent.parent / "data" / "raw"

def get_log_dir():
    """
    Determine the correct logs path depending on environment.
    """
    if os.environ.get("AIRFLOW_CTX_DAG_ID"):
        return Path("/opt/airflow/logs")
    else:
        return Path(__file__).parent.parent / "logs"

def setup_logging():
    """
    Configure logging, creating logs folder if necessary
    """
    log_dir = get_log_dir()
    log_dir.mkdir(exist_ok=True, parents=True)
    
    logging.basicConfig(
        filename=log_dir / 'pipeline.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        force=True  # Force reconfiguration in case already configured
    )
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

def run_pipeline():
    """
    Run full ETL: extract, transform, validate, load
    """
    RAW_DATA_DIR = get_raw_data_dir()
    setup_logging()
    
    logging.info("🚀 Starting Stock ETL Pipeline...")
    print("🚀 Starting Stock ETL Pipeline...")
    
    # Check if raw data directory exists
    if not RAW_DATA_DIR.exists():
        error_msg = f"Raw data directory not found: {RAW_DATA_DIR}"
        logging.error(error_msg)
        print(f"❌ {error_msg}")
        raise FileNotFoundError(error_msg)
    
    csv_files = list(RAW_DATA_DIR.glob("*.csv"))
    
    if not csv_files:
        warning_msg = f"No CSV files found in {RAW_DATA_DIR}"
        logging.warning(warning_msg)
        print(f"⚠️ {warning_msg}")
        return
    
    logging.info(f"Found {len(csv_files)} CSV file(s) to process")
    print(f"📁 Found {len(csv_files)} CSV file(s) to process")
    
    success_count = 0
    error_count = 0
    
    for file_path in csv_files:
        logging.info(f"Processing file: {file_path.name}")
        print(f"\n📄 Processing file: {file_path.name}")
        
        try:
            # Extract: Read CSV
            logging.info(f"  → Reading CSV...")
            df = pd.read_csv(file_path, sep=",", header=0, encoding="utf-8")
            logging.info(f"  → Read {len(df)} rows")
            print(f"  📥 Read {len(df)} rows")
            
            # Transform data
            logging.info(f"  → Transforming data...")
            df = transform(df)
            print(f"  🔄 Transformed data")
            
            # Validate data
            logging.info(f"  → Validating data...")
            validate(df)
            print(f"  ✅ Validation passed")
            
            # Load data
            logging.info(f"  → Loading to database...")
            load(df)
            print(f"  📤 Loaded to database")
            
            logging.info(f"✅ {file_path.name} loaded successfully")
            print(f"✨ {file_path.name} processed successfully")
            success_count += 1
            
        except Exception as e:
            error_count += 1
            logging.error(f"❌ Error processing {file_path.name}: {str(e)}", exc_info=True)
            print(f"❌ Error on {file_path.name}: {str(e)}")
            # Continue processing other files even if one fails
            continue
    
    # Summary
    summary_msg = f"Pipeline completed: {success_count} succeeded, {error_count} failed"
    logging.info(summary_msg)
    print(f"\n{'='*60}")
    print(f"📊 {summary_msg}")
    print(f"{'='*60}")
    
    if error_count > 0:
        raise Exception(f"Pipeline completed with {error_count} error(s)")

if __name__ == "__main__":
    run_pipeline()