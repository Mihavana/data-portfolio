import pandas as pd

def transform(df : pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(df["Date"], utc=True, errors='coerce').dt.tz_localize(None)

    numeric_cols = [
        "Open", "High", "Low", "Close",
        "Volume", "Dividends", "Stock Splits"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
        "Dividends": "dividends",
        "Stock Splits": "stock_splits"
    })

    df = df[
        [
            "symbol", "date", "open", "high",
            "low", "close", "volume",
            "dividends", "stock_splits",
            "extracted_at"
        ]
    ]

    df = df.drop_duplicates(subset=["symbol", "date"])

    return df