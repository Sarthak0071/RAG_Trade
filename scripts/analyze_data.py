# Data structure analysis for Phase 2 prompt engineering

import pandas as pd
import sys

def analyze_data():
    # Load data
    print("Loading data...")
    df = pd.read_csv('data/done_des.csv')
    
    print(f"\n{'='*60}")
    print("DATA STRUCTURE ANALYSIS")
    print(f"{'='*60}\n")
    
    # Basic stats
    print(f"Total Records: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nSchema:")
    print(df.dtypes.to_string())
    
    # Data ranges
    print(f"\n{'='*60}")
    print("DATA RANGES")
    print(f"{'='*60}\n")
    print(f"Years: {df['Year'].min()} to {df['Year'].max()}")
    print(f"Months: {df['Month'].min()} to {df['Month'].max()}")
    print(f"Directions: {df['Direction'].unique()}")
    
    # Top insights
    print(f"\n{'='*60}")
    print("KEY INSIGHTS FOR SQL PROMPTS")
    print(f"{'='*60}\n")
    
    # Country analysis
    print(f"Countries: {df['Country'].nunique()} unique")
    print(f"Top 10 countries by record count:")
    top_countries = df['Country'].value_counts().head(10)
    for country, count in top_countries.items():
        print(f"  {country}: {count:,} records")
    
    # HS Code analysis
    print(f"\nHS Codes: {df['HS_Code'].nunique():,} unique")
    print(f"Top 10 HS codes:")
    top_hs = df['HS_Code'].value_counts().head(10)
    for hs, count in top_hs.items():
        print(f"  {hs}: {count:,} records")
    
    # Direction breakdown
    print(f"\nDirection Breakdown:")
    dir_counts = df['Direction'].value_counts()
    for direction, count in dir_counts.items():
        dir_name = "Import" if direction == 'I' else "Export"
        print(f"  {dir_name} ({direction}): {count:,} records")
    
    # Value analysis
    print(f"\nValue (NPR):")
    print(f"  Total: NPR {df['Value'].sum():,.2f}")
    print(f"  Average: NPR {df['Value'].mean():,.2f}")
    print(f"  Max: NPR {df['Value'].max():,.2f}")
    print(f"  Records with Value > 0: {(df['Value'] > 0).sum():,}")
    
    # Quantity analysis
    print(f"\nQuantity:")
    print(f"  Total: {df['Quantity'].sum():,.2f}")
    print(f"  Average: {df['Quantity'].mean():,.2f}")
    print(f"  Records with Quantity > 0: {(df['Quantity'] > 0).sum():,}")
    
    # Unit analysis
    print(f"\nUnits: {df['Unit'].nunique()} unique")
    print(f"Top 10 units:")
    top_units = df['Unit'].value_counts().head(10)
    for unit, count in top_units.items():
        print(f"  {unit}: {count:,} records")
    
    # Description analysis
    print(f"\nDescriptions: {df['Description'].nunique():,} unique")
    print(f"Sample descriptions (lowercase):")
    for desc in df['Description'].dropna().head(5):
        print(f"  {desc[:60]}...")
    
    # Year-Month breakdown
    print(f"\n{'='*60}")
    print("YEAR-MONTH DISTRIBUTION")
    print(f"{'='*60}\n")
    year_month = df.groupby(['Year', 'Month']).size().reset_index(name='count')
    for year in sorted(df['Year'].unique()):
        year_data = year_month[year_month['Year'] == year]
        months = year_data['Month'].tolist()
        total = year_data['count'].sum()
        print(f"Year {year}: {len(months)} months, {total:,} records")
    
    # Common queries
    print(f"\n{'='*60}")
    print("COMMON QUERY PATTERNS FOR PHASE 2")
    print(f"{'='*60}\n")
    
    queries = [
        "Total trade value by year",
        "Import vs Export by year",
        "Top trading partners (countries)",
        "Trade by specific HS code",
        "Monthly trade trends",
        "Trade with specific country",
        "Average trade value per month",
        "Total quantity by commodity",
        "Revenue analysis (imports only)",
        "Year-over-year growth"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"{i:2d}. {query}")
    
    # Critical notes for prompts
    print(f"\n{'='*60}")
    print("CRITICAL NOTES FOR SQL PROMPTS")
    print(f"{'='*60}\n")
    
    notes = [
        "Direction: 'I' = Import, 'E' = Export",
        "Country codes are ISO-2 (e.g., IN, CN, US)",
        "Years are Nepali fiscal years (2077-2082)",
        "Months are 1-12 (Nepali calendar)",
        "Descriptions are lowercase",
        "Revenue only exists for imports ('I')",
        "Value is in NPR (Nepalese Rupees)",
        "HS_Code is string type (can have leading zeros)",
        "Some records may have Value=0 OR Quantity=0 (but not both)",
        "Table name in DuckDB: 'trade'"
    ]
    
    for note in notes:
        print(f"  - {note}")
    
    print(f"\n{'='*60}")
    print("Analysis complete. Ready for Phase 2 prompt engineering.")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    try:
        analyze_data()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
