from db import get_connection

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