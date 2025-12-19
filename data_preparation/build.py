# Build done_des.csv from Excel files

import pandas as pd
from pathlib import Path
from .config import EXCEL_BASE_DIR, FISCAL_YEARS, MONTH_ORDER, OUTPUT_DIR, NEPALI_MONTHS
from .excel_reader import read_excel_file
from .processor import prepare_dataframe, calculate_monthly
from .metadata import get_files_with_metadata


def discover_files():
    # Find all Excel files by fiscal year
    files_by_year = {}
    
    for year_dir in FISCAL_YEARS:
        year_path = EXCEL_BASE_DIR / year_dir
        if not year_path.exists():
            print(f"Directory not found: {year_path}")
            continue
        
        excel_files = list(year_path.glob('*.xlsx')) + list(year_path.glob('*.xls'))
        files_by_year[year_dir] = sorted(excel_files)
        print(f"Found {len(excel_files)} files in {year_dir}")
    
    return files_by_year


def process_fiscal_year(year_dir: str, files: list) -> list:
    # Process all months in fiscal year
    base_year = int('20' + year_dir.split('-')[0])
    next_year = base_year + 1
    
    print(f"\nProcessing {year_dir} ({base_year}-{next_year})")
    
    # Extract metadata from files
    print("Extracting metadata...")
    files_metadata = get_files_with_metadata(files, year_dir)
    print(f"Extracted metadata from {len(files_metadata)} files")
    
    # Show files by month
    for fm in sorted(files_metadata, key=lambda x: x['month']):
        print(f"  Month {fm['month']:2d} ({NEPALI_MONTHS[fm['month']]:8s}): {fm['path'].name}")
    
    all_monthly_data = []
    previous_cumulative = None
    
    # Process in fiscal month order
    for month in MONTH_ORDER:
        # Find file for this month
        file_meta = None
        for fm in files_metadata:
            if fm['month'] == month:
                file_meta = fm
                break
        
        if not file_meta:
            print(f"  Month {month}: No file found")
            continue
        
        file_path = file_meta['path']
        year_num = file_meta['year']
        
        print(f"  Month {month}: {file_path.name} -> Year {year_num}")
        
        import_df, export_df = read_excel_file(file_path)
        
        import_cum = prepare_dataframe(import_df, 'I', year_num, month)
        export_cum = prepare_dataframe(export_df, 'E', year_num, month)
        
        current_cumulative = pd.concat([import_cum, export_cum], ignore_index=True)
        
        if current_cumulative.empty:
            print(f"    No data extracted")
            continue
        
        print(f"    Cumulative: {len(current_cumulative)} records")
        
        monthly_df = calculate_monthly(current_cumulative, previous_cumulative, year_num, month)
        
        if not monthly_df.empty:
            all_monthly_data.append(monthly_df)
            print(f"    Monthly: {len(monthly_df)} records")
        
        previous_cumulative = current_cumulative.copy()
    
    print(f"{year_dir} complete: {len(all_monthly_data)} months processed\n")
    return all_monthly_data


def main():
    # Main execution
    print("Building done_des.csv...\n")
    
    files_by_year = discover_files()
    all_data = []
    
    for year_dir in FISCAL_YEARS:
        if year_dir not in files_by_year:
            continue
        
        monthly_data = process_fiscal_year(year_dir, files_by_year[year_dir])
        all_data.extend(monthly_data)
    
    # Combine
    print("\nCombining all data...")
    done_df = pd.concat(all_data, ignore_index=True)
    print(f"Total records before cleaning: {len(done_df):,}")
    
    # Clean - Remove records where BOTH Value=0 AND Quantity=0
    print("\nCleaning zero-value records...")
    both_zero = (done_df['Value'] == 0) & (done_df['Quantity'] == 0)
    print(f"Records with Value=0 AND Quantity=0: {both_zero.sum():,}")
    done_df = done_df[~both_zero].copy()
    print(f"After removing zeros: {len(done_df):,}")
    
    # Fix tiny rounding errors
    tiny_values = (done_df['Value'].abs() < 0.01) & (done_df['Value'] != 0)
    tiny_qty = (done_df['Quantity'].abs() < 0.01) & (done_df['Quantity'] != 0)
    print(f"Tiny rounding errors - Value: {tiny_values.sum():,}, Quantity: {tiny_qty.sum():,}")
    done_df.loc[tiny_values, 'Value'] = 0.0
    done_df.loc[tiny_qty, 'Quantity'] = 0.0
    
    # Remove nulls
    done_df = done_df[done_df['HS_Code'].notna()]
    done_df = done_df[done_df['Country'].notna()]
    
    # Types
    done_df['Year'] = done_df['Year'].astype(int)
    done_df['Month'] = done_df['Month'].astype(int)
    done_df['Value'] = pd.to_numeric(done_df['Value'], errors='coerce').fillna(0)
    done_df['Quantity'] = pd.to_numeric(done_df['Quantity'], errors='coerce').fillna(0)
    done_df['Unit'] = done_df['Unit'].str.lower()
    
    # Final columns
    final_cols = ['Year', 'Month', 'Direction', 'HS_Code', 'Description', 'Country', 
                  'Value', 'Quantity', 'Unit']
    if 'Revenue' in done_df.columns:
        final_cols.append('Revenue')
    
    done_df = done_df[final_cols]
    
    print(f"Total records after cleaning: {len(done_df):,}")
    
    # Save
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / 'done_des.csv'
    done_df.to_csv(output_path, index=False)
    
    print(f"\nSaved to: {output_path}")
    print(f"Final row count: {len(done_df):,}")
    
    # Summary
    print("\nBreakdown by year:")
    summary = done_df.groupby(['Year', 'Direction']).size().unstack(fill_value=0)
    print(summary)
    
    return done_df


if __name__ == '__main__':
    main()
