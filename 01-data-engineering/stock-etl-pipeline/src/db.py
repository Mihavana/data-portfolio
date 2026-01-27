# src/db.py
import psycopg2
import os

def get_connection():
    """Créer une connexion à la base de données"""
    # Utiliser les variables d'environnement
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),      # ← Important
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'portfolio_db'),
        user=os.getenv('DB_USER', 'user'),
        password=os.getenv('DB_PASSWORD', 'password')
    )
    return conn