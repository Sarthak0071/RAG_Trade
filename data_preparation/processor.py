# Data processor

import pandas as pd
from pathlib import Path
from typing import List, Tuple
from .utils import get_iso2_code
from .config import MONTH_ORDER


def prepare_dataframe(df: pd.DataFrame, direction: str, year: int, month: int) -> pd.DataFrame:
    # Prepare DataFrame with metadata
    if df is None or df.empty:
        return pd.DataFrame()
    
    df = df.copy()
    df['Year'] = year
    df['Month'] = month
    df['Direction'] = direction
    
    # Ensure columns exist
    if 'Unit' not in df.columns:
        df['Unit'] = 'pcs'
    if 'Quantity' not in df.columns:
        df['Quantity'] = 0
    if direction == 'I' and 'Revenue' not in df.columns:
        df['Revenue'] = 0
    if 'Description' not in df.columns:
        df['Description'] = ''
    
    # Clean HS codes
    df['HS_Code'] = df['HS_Code'].astype(str).str.replace('.0', '', regex=False)
    
    # Convert countries to ISO-2
    df['Country'] = df['Country'].apply(get_iso2_code)
    
    return df


def calculate_monthly(current_df: pd.DataFrame, previous_df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    # Calculate monthly values from cumulative
    
    if current_df.empty:
        return pd.DataFrame()
    
    current_df = current_df.copy()
    current_df['_key'] = (
        current_df['HS_Code'].astype(str) + '|' +
        current_df['Country'].astype(str) + '|' +
        current_df['Direction'].astype(str)
    )
    
    agg_dict = {
        'HS_Code': 'first',
        'Country': 'first',
        'Direction': 'first',
        'Description': 'first',
        'Value': 'sum',
        'Quantity': 'sum',
        'Unit': 'first'
    }
    if 'Revenue' in current_df.columns:
        agg_dict['Revenue'] = 'sum'
    
    current_agg = current_df.groupby('_key', as_index=False).agg(agg_dict)
    current_dict = current_agg.set_index('_key').to_dict('index')
    
    # If no previous (Shrawan), return current as monthly
    if previous_df is None or previous_df.empty:
        result = current_agg.copy()
        result['Year'] = year
        result['Month'] = month
        result.drop(columns=['_key'], inplace=True, errors='ignore')
        return result
    
    # Aggregate previous
    previous_df = previous_df.copy()
    previous_df['_key'] = (
        previous_df['HS_Code'].astype(str) + '|' +
        previous_df['Country'].astype(str) + '|' +
        previous_df['Direction'].astype(str)
    )
    
    previous_agg = previous_df.groupby('_key', as_index=False).agg(agg_dict)
    previous_dict = previous_agg.set_index('_key').to_dict('index')
    
    # Calculate differences
    monthly_records = []
    all_keys = set(current_dict.keys()) | set(previous_dict.keys())
    
    for key in all_keys:
        curr = current_dict.get(key, {})
        prev = previous_dict.get(key, {})
        
        if not curr:
            continue
        
        monthly_value = curr.get('Value', 0) - prev.get('Value', 0)
        monthly_quantity = curr.get('Quantity', 0) - prev.get('Quantity', 0)
        
        record = {
            'Year': year,
            'Month': month,
            'Direction': curr['Direction'],
            'HS_Code': curr['HS_Code'],
            'Description': curr.get('Description', ''),
            'Country': curr['Country'],
            'Value': monthly_value,
            'Quantity': monthly_quantity,
            'Unit': curr.get('Unit', 'pcs')
        }
        
        if 'Revenue' in curr:
            record['Revenue'] = curr.get('Revenue', 0) - prev.get('Revenue', 0)
        
        monthly_records.append(record)
    
    return pd.DataFrame(monthly_records)
