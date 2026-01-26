# src/validate.py
import pandas as pd

def validate(df):
    df.columns = df.columns.str.strip().str.lower()

    errors = []

    # Define expected columns
    expected_cols = ["date", "open", "high", "low", "close", "volume", 
                     "dividends", "stock_splits", "symbol", "extracted_at"]

    # Verify expected columns exist
    for col in expected_cols:
        if col not in df.columns:
            errors.append(f"Missing expected column: '{col}'")

    # Check for missing values
    if "date" in df.columns and df["date"].isnull().any():
        errors.append("Missing values found in 'date' column")
    if "symbol" in df.columns and df["symbol"].isnull().any():
        errors.append("Missing values found in 'symbol' column")
    
    # Check data types
    if "date" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["date"]):
        errors.append("'date' column is not datetime")
    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
            errors.append(f"'{col}' column is not numeric")
    
    # Check logical constraints
    if "high" in df.columns and "low" in df.columns and (df["high"] < df["low"]).any():
        errors.append("Some rows have High < Low")
    numeric_cols = [c for c in ["open","high","low","close","volume"] if c in df.columns]
    if (df[numeric_cols] < 0).any().any():
        errors.append("Negative values found in price/volume columns")

    # Check duplicates
    if "symbol" in df.columns and "date" in df.columns:
        duplicates = df.duplicated(subset=["symbol", "date"]).sum()
        if duplicates > 0:
            errors.append(f"{duplicates} duplicate rows based on (symbol, date)")

    if errors:
        raise ValueError("Data validation failed:\n" + "\n".join(errors))
    
    print("✅ Data validation passed")
    return True
