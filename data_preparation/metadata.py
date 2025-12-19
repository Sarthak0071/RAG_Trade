# Metadata extraction from Excel headers

import pandas as pd
import re
from pathlib import Path
from typing import Optional, Dict
from .config import IMPORT_SHEET_KEYS

# Month name mappings
MONTH_NAME_TO_NUM = {
    'Baishakh': 1, 'Baisakh': 1,
    'Jestha': 2, 'Jeth': 2, 'Jetha': 2,
    'Ashad': 3, 'Asar': 3, 'Ashar': 3,
    'Shrawan': 4, 'Srawan': 4,
    'Bhadra': 5,
    'Ashwin': 6, 'Asoj': 6, 'Aswin': 6,
    'Kartik': 7,
    'Mangsir': 8, 'Mangshir': 8,
    'Poush': 9, 'Push': 9, 'Paush': 9,
    'Magh': 10,
    'Falgun': 11, 'Fagun': 11, 'Phalgun': 11,
    'Chaitra': 12, 'Chait': 12
}

# Filename patterns for fallback
MONTH_PATTERNS = {
    4: ['shrawan', 'श्रावण', '04_', '_04'],
    5: ['bhadra', 'भाद्र'],
    6: ['asoj', 'ashwin'],
    7: ['kartik'],
    8: ['mangsir'],
    9: ['poush', 'push'],
    10: ['magh'],
    11: ['falgun', 'fagun'],
    12: ['chaitra'],
    1: ['baishakh'],
    2: ['jestha'],
    3: ['ashad', 'asad', 'annual']
}


def find_sheet(sheet_names: list, keywords: list) -> Optional[str]:
    # Find sheet matching keywords
    for sheet in sheet_names:
        if any(kw in sheet.lower() for kw in keywords):
            return sheet
    return None


def extract_metadata_from_header(excel_path: Path, fiscal_year_dir: str) -> Optional[Dict]:
    # Extract fiscal year and month from Excel header
    try:
        xls = pd.ExcelFile(excel_path)
        import_sheet = find_sheet(xls.sheet_names, IMPORT_SHEET_KEYS)
        
        if not import_sheet:
            return None
        
        df_header = pd.read_excel(excel_path, sheet_name=import_sheet, nrows=15, header=None)
        
        fiscal_year_start = None
        fiscal_year_end = None
        end_month = None
        
        # Search for header
        for idx, row in df_header.iterrows():
            for cell_value in row:
                if pd.isna(cell_value):
                    continue
                
                cell_text = str(cell_value)
                
                # Find fiscal year
                if not fiscal_year_start:
                    fy_match = re.search(r'(?:FY\s*)?(\d{4})[/\-](\d{2,4})', cell_text, re.IGNORECASE)
                    if fy_match:
                        fiscal_year_start = int(fy_match.group(1))
                        fy_end_str = fy_match.group(2)
                        fiscal_year_end = int('20' + fy_end_str) if len(fy_end_str) == 2 else int(fy_end_str)
                
                # Find month in parentheses
                if end_month is None:
                    paren_match = re.search(r'\(([^)]+)\)', cell_text)
                    if paren_match:
                        range_text = paren_match.group(1)
                        
                        if '-' in range_text:
                            parts = range_text.split('-')
                            end_month_text = parts[-1].strip()
                        else:
                            end_month_text = range_text.strip()
                        
                        # Match month name
                        for month_variant, m_num in MONTH_NAME_TO_NUM.items():
                            if month_variant.lower() in end_month_text.lower():
                                end_month = m_num
                                break
                
                if fiscal_year_start and end_month:
                    break
            
            if fiscal_year_start and end_month:
                break
        
        # Calculate actual year
        if fiscal_year_start and end_month:
            actual_year = fiscal_year_start if end_month >= 4 else fiscal_year_end
            return {
                'fiscal_year_start': fiscal_year_start,
                'fiscal_year_end': fiscal_year_end,
                'month': end_month,
                'year': actual_year
            }
        
        # Fallback to filename
        base_year = int('20' + fiscal_year_dir.split('-')[0])
        next_year = base_year + 1
        fname = excel_path.name.lower()
        
        for m_num, patterns in MONTH_PATTERNS.items():
            if any(p in fname for p in patterns):
                actual_year = base_year if m_num >= 4 else next_year
                return {
                    'fiscal_year_start': base_year,
                    'fiscal_year_end': next_year,
                    'month': m_num,
                    'year': actual_year
                }
        
        return None
        
    except Exception as e:
        return None


def get_files_with_metadata(files: list, fiscal_year_dir: str) -> list:
    # Extract metadata from all files
    files_metadata = []
    
    for file_path in files:
        metadata = extract_metadata_from_header(file_path, fiscal_year_dir)
        if metadata:
            files_metadata.append({
                'path': file_path,
                'month': metadata['month'],
                'year': metadata['year'],
                'fiscal_year_start': metadata['fiscal_year_start'],
                'fiscal_year_end': metadata['fiscal_year_end']
            })
    
    return files_metadata
