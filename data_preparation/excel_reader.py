# Excel file reader

import pandas as pd
from pathlib import Path
from typing import Optional, List, Tuple
from .utils import standardize_columns, map_columns, to_numeric_safe
from .config import IMPORT_SHEET_KEYS, EXPORT_SHEET_KEYS


def find_sheet(sheet_names: List[str], keywords: List[str]) -> Optional[str]:
    # Find sheet matching keywords
    for sheet in sheet_names:
        sheet_lower = sheet.lower()
        if any(kw in sheet_lower for kw in keywords):
            return sheet
    return None


def find_data_start(df_sample: pd.DataFrame) -> int:
    # Find row where data starts
    for idx, row in df_sample.iterrows():
        row_str = ' '.join(str(val).lower() for val in row[:3] if pd.notna(val))
        if 'hscode' in row_str or 'hs_code' in row_str or 'code' in row_str:
            return idx
    return 0


def read_trade_sheet(excel_path: Path, sheet_keys: List[str], trade_type: str) -> Optional[pd.DataFrame]:
    # Read import or export sheet from Excel
    try:
        xls = pd.ExcelFile(excel_path)
        sheet_names = xls.sheet_names
        
        target_sheet = find_sheet(sheet_names, sheet_keys)
        if not target_sheet:
            return None
        
        df_sample = pd.read_excel(excel_path, sheet_name=target_sheet, nrows=10, header=None)
        skip_rows = find_data_start(df_sample)
        
        df = pd.read_excel(excel_path, sheet_name=target_sheet, skiprows=skip_rows)
        df = standardize_columns(df)
        
        column_mapping = {
            'HS_Code': ['hscode', 'hs_code', 'code', 'hs'],
            'Description': ['description', 'commodity', 'item'],
            'Country': ['partner', 'country', 'countries'],
            'Unit': ['unit'],
            'Quantity': ['quantity'],
            'Value': ['value'],
            'Revenue': ['revenue']
        }
        
        df = map_columns(df, column_mapping)
        
        # Add defaults
        if 'Unit' not in df.columns:
            df['Unit'] = 'pcs'
        if 'Quantity' not in df.columns:
            df['Quantity'] = 0
        if trade_type == 'import' and 'Revenue' not in df.columns:
            df['Revenue'] = 0
        if 'Description' not in df.columns:
            df['Description'] = ''
        
        # Clean
        df = df[df['HS_Code'].notna()]
        df = df.dropna(how='all')
        
        # Convert types
        for col in ['Value', 'Quantity', 'Revenue']:
            if col in df.columns:
                df[col] = to_numeric_safe(df[col])
        
        df['HS_Code'] = df['HS_Code'].astype(str).str.strip().str.replace('.0', '', regex=False)
        df['Country'] = df['Country'].astype(str).str.strip()
        df['Description'] = df['Description'].astype(str).str.strip()
        
        return df
        
    except Exception as e:
        return None


def read_excel_file(excel_path: Path) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    # Read both import and export data
    import_df = read_trade_sheet(excel_path, IMPORT_SHEET_KEYS, 'import')
    export_df = read_trade_sheet(excel_path, EXPORT_SHEET_KEYS, 'export')
    
    return import_df, export_df
