# Data preparation configuration

import sys
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent.parent.parent  # Go to All/ folder
EXCEL_BASE_DIR = ROOT_DIR
OUTPUT_DIR = Path(__file__).parent.parent / "data"

# Fiscal years to process
FISCAL_YEARS = ['77-78', '78-79', '79-80', '80-81', '81-82', '82-83']

# Month processing order (Nepali fiscal year)
MONTH_ORDER = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]

# Nepali month names
NEPALI_MONTHS = {
    1: 'Baishakh', 2: 'Jestha', 3: 'Ashad', 4: 'Shrawan',
    5: 'Bhadra', 6: 'Ashwin', 7: 'Kartik', 8: 'Mangsir',
    9: 'Poush', 10: 'Magh', 11: 'Falgun', 12: 'Chaitra'
}

# Sheet keywords for Excel files
IMPORT_SHEET_KEYS = ['4', 'import', 'table 4']
EXPORT_SHEET_KEYS = ['6', 'export', 'table 6']

# Country code mappings
CUSTOM_COUNTRY_MAP = {
    'Namibia': 'NA',
    'Yugoslavia': 'RS',
    'Zaire': 'CD',
    'Swaziland': 'SZ',
    'Kazakstan': 'KZ',
    'Viet Nam': 'VN',
    'Libyan Arab Jamahiriya': 'LY',
    'Holy See (Vatican)': 'VA',
    'Brunei Darussalam': 'BN',
    "Cote d'Ivoire": 'CI',
    'Turkey': 'TR',
    'Congo': 'CG',
    'East Timor': 'TL',
    'Kosovo': 'XK',
    'Taiwan, Province of China': 'TW',
    'Serbia (Europe)': 'RS',
    'The former Yugoslav Rep. Macedonia': 'MK',
    'Many Countries': 'MANY',
    'Not_Specified': 'NOT_SPECIFIED',
}
