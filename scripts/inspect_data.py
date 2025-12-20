import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "done_des.csv"

def inspect_done_des():
    print(f"Inspecting: {DATA_PATH}\n")
    
    # Load first 1000 rows for schema and sample data
    df = pd.read_csv(DATA_PATH, nrows=1000)
    
    print("COLUMNS:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col} ({df[col].dtype})")
    
    print(f"\nTOTAL COLUMNS: {len(df.columns)}")
    print(f"ROW COUNT (sample): {len(df)}")
    
    # Get total row count
    row_count = sum(1 for _ in open(DATA_PATH, encoding='utf-8')) - 1
    print(f"TOTAL ROWS: {row_count:,}")
    
    print("\nSAMPLE DATA (first 3 rows):")
    print(df.head(3).to_string(index=False))
    
    print("\nUNIQUE VALUES CHECK:")
    for col in df.columns:
        unique_count = df[col].nunique()
        if unique_count < 20:
            print(f"  {col}: {unique_count} unique values")
            print(f"    Values: {df[col].unique().tolist()[:10]}")
    
    print("\nDATA TYPES SUMMARY:")
    print(df.dtypes)
    
    print("\nNULL VALUES:")
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        print(null_counts[null_counts > 0])
    else:
        print("  No null values in sample")

if __name__ == "__main__":
    inspect_done_des()
