# src/load.py
from psycopg2.extras import execute_values
from db import get_connection

def load(df):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO stocks (
            symbol, date, open, high, low,
            close, volume, dividends,
            stock_splits, extracted_at
        )
        VALUES %s
        ON CONFLICT (symbol, date) DO NOTHING;
    """

    values = [tuple(row) for row in df.to_numpy()]
    execute_values(cursor, query, values)

    conn.commit()
    cursor.close()
    conn.close()
