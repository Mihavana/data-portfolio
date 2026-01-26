# src/main.py
import pandas as pd
from pathlib import Path
from transform import transform
from load import load

RAW_DATA_DIR = Path(
    "/mnt/44D2A11AD2A1116A/Portfolio/data-portfolio/data-engineering/stock-etl-pipeline/data/raw"
)

csv_files = list(RAW_DATA_DIR.glob("*.csv"))

if not csv_files:
    print("Aucun fichier CSV trouvé.")
    exit()

for file_path in csv_files:
    print(f"Traitement du fichier : {file_path.name}")

    try:
        df = pd.read_csv(
            file_path,
            sep=",",
            encoding="utf-8"
        )

        df = transform(df)
        load(df)

        print(f"✅ {file_path.name} chargé avec succès\n")

    except Exception as e:
        print(f"❌ Erreur sur {file_path.name} : {e}\n")
