from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def run_etl_main():

    import pandas as pd
    from pathlib import Path

    from src.db import get_connection
    from src.transform import transform
    from src.load import load
    from src.validate import validate
    
    print("=" * 80)
    print("DÉBUT DU PIPELINE SIMPLE")
    print("=" * 80)
    
    # 1. Configuration
    print("🚀 Starting Stock ETL Pipeline...")

    RAW_DATA_DIR = Path("/opt/airflow/data/raw")
    print(f"Dossier data : {RAW_DATA_DIR}")
    print(f"Existe : {RAW_DATA_DIR.exists()}")
    
    csv_files = list(RAW_DATA_DIR.glob("*.csv"))
    
    if not csv_files:
        print("❌ Aucun fichier CSV trouvé !")
        return "No CSV files found"
    
    print(f"✅ Trouvé {len(csv_files)} fichiers CSV")
    for f in csv_files:
        print(f"  - {f.name}")
    
    success_count = 0
    error_count = 0

    for file_path in csv_files:
        print(f"\n📄 Processing file: {file_path.name}")
        
        try:
            # Extract: Read CSV
            df = pd.read_csv(file_path, sep=",", header=0, encoding="utf-8")
            # logging.info(f"  → Read {len(df)} rows")
            print(f"  📥 Read {len(df)} rows")
            
            # Transform data
            # logging.info(f"  → Transforming data...")
            df = transform(df)
            print(f"  🔄 Transformed data")
            
            # Validate data
            # logging.info(f"  → Validating data...")
            validate(df)
            print(f"  ✅ Validation passed")
            
            # Load data
            # logging.info(f"  → Loading to database...")
            load(df)
            print(f"  📤 Loaded to database")
            
            # logging.info(f"✅ {file_path.name} loaded successfully")
            print(f"✨ {file_path.name} processed successfully")
            success_count += 1
            
        except Exception as e:
            error_count += 1
            # logging.error(f"❌ Error processing {file_path.name}: {str(e)}", exc_info=True)
            print(f"❌ Error on {file_path.name}: {str(e)}")
            # Continue processing other files even if one fails
            continue
    
    summary_msg = f"Pipeline completed: {success_count} succeeded, {error_count} failed"
    # logging.info(summary_msg)
    print(f"\n{'='*60}")
    print(f"📊 {summary_msg}")
    print(f"{'='*60}")
    
    if error_count > 0:
        raise Exception(f"Pipeline completed with {error_count} error(s)")

with DAG(
    dag_id='stock_etl_pipeline_main',
    start_date=datetime(2026, 1, 26),
    schedule_interval=None,
    catchup=False,
    tags=['stocks', 'test'],
) as dag:
    
    task = PythonOperator(
        task_id='run_etl_main',
        python_callable=run_etl_main,
    )