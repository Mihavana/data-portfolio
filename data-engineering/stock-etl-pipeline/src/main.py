# src/main.py
import pandas as pd
from pathlib import Path
from transform import transform
from load import load
from validate import validate
import logging

RAW_DATA_DIR = Path(
    "/mnt/44D2A11AD2A1116A/Portfolio/data-portfolio/data-engineering/stock-etl-pipeline/data/raw"
)

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

csv_files = list(RAW_DATA_DIR.glob("*.csv"))

if not csv_files:
    logging.warning("Aucun fichier CSV trouvé.")
    print("Aucun fichier CSV trouvé.")
    exit()

for file_path in csv_files:
    logging.info(f"Processing file: {file_path.name}")
    print(f"Traitement du fichier : {file_path.name}")

    try:
        df = pd.read_csv(
            file_path,
            sep=",",
            header=0,
            encoding="utf-8"
        )

        # Transformation des données
        df = transform(df)

        # Validation des données transformées
        validate(df)

        # Chargement des données validées
        load(df)

        logging.info(f"{file_path.name} loaded successfully")
        print(f"✅ {file_path.name} loaded successfully\n")

    except Exception as e:
        logging.error(f"Error on {file_path.name}: {e}")
        print(f"❌ Error on {file_path.name} : {e}\n")
