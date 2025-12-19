# Utility functions for data processing

import pandas as pd
import pycountry
from typing import Dict, List
from .config import CUSTOM_COUNTRY_MAP


def get_iso2_code(country_name: str) -> str:
    # Convert country name to ISO-2 code
    if pd.isna(country_name):
        return country_name
    
    country_name = str(country_name).strip()
    
    # Check custom mappings
    if country_name in CUSTOM_COUNTRY_MAP:
        return CUSTOM_COUNTRY_MAP[country_name]
    
    # Try exact match
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            return country.alpha_2
    except:
        pass
    
    # Try fuzzy search
    try:
        results = pycountry.countries.search_fuzzy(country_name)
        if results:
            return results[0].alpha_2
    except:
        pass
    
    return country_name


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df


def to_numeric_safe(series: pd.Series) -> pd.Series:
    # Convert to numeric with error handling
    return pd.to_numeric(series, errors='coerce').fillna(0)


def find_column(df: pd.DataFrame, keywords: List[str]) -> str:
    # Find column matching keywords
    for col in df.columns:
        col_clean = str(col).lower().replace('_', '').replace(' ', '')
        if any(kw.replace('_', '') in col_clean for kw in keywords):
            return col
    return None


def map_columns(df: pd.DataFrame, column_map: Dict[str, List[str]]) -> pd.DataFrame:
    # Map columns using keywords
    rename_dict = {}
    
    for target_col, keywords in column_map.items():
        found_col = find_column(df, keywords)
        if found_col:
            rename_dict[found_col] = target_col
    
    return df.rename(columns=rename_dict)
