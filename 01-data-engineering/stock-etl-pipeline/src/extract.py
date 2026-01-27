# src/extract.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

RAW_DATA_PATH = Path("/opt/airflow/data/raw")

def extract_stock_data(symbol: str, start: str = "2022-01-01") -> Path:
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start)

    df.reset_index(inplace=True)
    df["symbol"] = symbol
    df["extracted_at"] = datetime.now(timezone.utc)

    output_file = RAW_DATA_PATH / f"{symbol}_{datetime.now(timezone.utc)}.csv"
    df.to_csv(output_file, index=False, sep=",", encoding="utf-8")

    return output_file


if __name__ == "__main__":
    symbols = ["AAPL", "MSFT", "GOOGL"]

    for symbol in symbols:
        path = extract_stock_data(symbol)
        print(f"Extracted data saved to {path}")
