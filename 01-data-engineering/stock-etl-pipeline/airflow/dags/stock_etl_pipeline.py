from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def run_etl_simple():
    """Version ultra-simplifiée avec debug"""
    import pandas as pd
    from pathlib import Path
    from src.db import get_connection
    
    print("=" * 80)
    print("DÉBUT DU PIPELINE SIMPLE")
    print("=" * 80)
    
    # 1. Configuration
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
    
    success = 0
    errors = 0
    error_messages = []
    
    # 2. Traiter chaque fichier
    for file_path in csv_files:
        print("\n" + "-" * 80)
        print(f"📄 Traitement de : {file_path.name}")
        print("-" * 80)
        
        try:
            # Lire CSV
            print(f"  1️⃣ Lecture du CSV...")
            df = pd.read_csv(file_path)
            print(f"     ✅ Lu {len(df)} lignes")
            print(f"     Colonnes: {list(df.columns)}")
            
            # Nettoyer colonnes
            print(f"  2️⃣ Nettoyage des colonnes...")
            df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
            print(f"     ✅ Colonnes nettoyées: {list(df.columns)}")
            
            # Convertir dates
            print(f"  3️⃣ Conversion des dates...")
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                print(f"     ✅ Dates converties")
            else:
                print(f"     ⚠️ Pas de colonne 'date'")
            
            # Supprimer doublons et NaN
            print(f"  4️⃣ Nettoyage des données...")
            initial_len = len(df)
            df = df.drop_duplicates()
            
            if 'symbol' in df.columns:
                df = df.dropna(subset=['date', 'symbol'])
            else:
                df = df.dropna(subset=['date'])
            
            print(f"     ✅ {initial_len} → {len(df)} lignes (après nettoyage)")
            
            # Charger dans la DB
            print(f"  5️⃣ Connexion à la base de données...")
            conn = get_connection()
            cursor = conn.cursor()
            print(f"     ✅ Connecté")
            
            print(f"  6️⃣ Insertion des données...")
            inserted = 0
            skipped = 0
            
            for idx, row in df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO stocks (symbol, date, open, high, low, close, volume, dividends, stock_splits, extracted_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (symbol, date) DO NOTHING
                    """, (
                        row.get('symbol'),
                        row.get('date'),
                        row.get('open'),
                        row.get('high'),
                        row.get('low'),
                        row.get('close'),
                        row.get('volume'),
                        row.get('dividends'),
                        row.get('stock_splits'),
                        row.get('extracted_at')
                    ))
                    
                    if cursor.rowcount > 0:
                        inserted += 1
                    else:
                        skipped += 1
                        
                except Exception as e:
                    print(f"     ⚠️ Erreur ligne {idx}: {e}")
                    continue
            
            conn.commit()
            conn.close()
            
            print(f"     ✅ {inserted} lignes insérées, {skipped} doublons ignorés")
            print(f"  ✅ Fichier traité avec succès !")
            success += 1
            
        except Exception as e:
            print(f"  ❌ ERREUR SUR LE FICHIER : {type(e).__name__}")
            print(f"     Message : {str(e)}")
            import traceback
            print(f"     Traceback :")
            traceback.print_exc()
            error_messages.append(f"{file_path.name}: {str(e)}")
            errors += 1
    
    print("\n" + "=" * 80)
    print(f"RÉSUMÉ FINAL")
    print("=" * 80)
    print(f"✅ Succès  : {success} fichiers")
    print(f"❌ Échecs  : {errors} fichiers")
    
    if error_messages:
        print("\nDétails des erreurs :")
        for msg in error_messages:
            print(f"  - {msg}")
    
    print("=" * 80)
    
    result = f"Done: {success} succeeded, {errors} failed"
    if error_messages:
        result += f" | Errors: {'; '.join(error_messages[:2])}"  # Limiter à 2 pour éviter message trop long
    
    return result

with DAG(
    dag_id='stock_etl_pipeline',
    start_date=datetime(2026, 1, 26),
    schedule_interval=None,
    catchup=False,
    tags=['stocks', 'test'],
) as dag:
    
    task = PythonOperator(
        task_id='run_etl_simple',
        python_callable=run_etl_simple,
    )