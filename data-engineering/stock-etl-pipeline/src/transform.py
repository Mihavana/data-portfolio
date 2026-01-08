import pandas as pd

def transform(df : pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()