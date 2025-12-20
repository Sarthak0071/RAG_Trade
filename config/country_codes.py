# Country name to ISO-2 code mapping for SQL generation

COUNTRY_MAPPINGS = {
    # Top trading partners
    'india': 'IN',
    'china': 'CN',
    'usa': 'US',
    'united states': 'US',
    'japan': 'JP',
    'germany': 'DE',
    'uk': 'GB',
    'united kingdom': 'GB',
    'britain': 'GB',
    'thailand': 'TH',
    'south korea': 'KR',
    'korea': 'KR',
    'uae': 'AE',
    'emirates': 'AE',
    'australia': 'AU',
    'malaysia': 'MY',
    'italy': 'IT',
    'france': 'FR',
    'qatar': 'QA',
    'hong kong': 'HK',
    'taiwan': 'TW',
    'vietnam': 'VN',
    'indonesia': 'ID',
    'singapore': 'SG',
    'saudi arabia': 'SA',
    'canada': 'CA',
    'switzerland': 'CH',
    'kuwait': 'KW',
    'bangladesh': 'BD',
    'netherlands': 'NL',
    'turkey': 'TR',
    'spain': 'ES',
    'israel': 'IL',
    'poland': 'PL',
    'austria': 'AT',
    'belgium': 'BE',
    'czech republic': 'CZ',
    'sweden': 'SE',
    'mexico': 'MX',
    'denmark': 'DK',
    'philippines': 'PH',
    'oman': 'OM',
    'bahrain': 'BH',
    'pakistan': 'PK',
    'uzbekistan': 'UZ',
    'new zealand': 'NZ',
    'hungary': 'HU',
    'ireland': 'IE',
    'finland': 'FI',
    'romania': 'RO',
    'norway': 'NO',
    'slovakia': 'SK',
    'brazil': 'BR',
    'portugal': 'PT',
    'south africa': 'ZA',
    'bhutan': 'BT',
    'sri lanka': 'LK',
    'bulgaria': 'BG',
    'cyprus': 'CY',
    'cambodia': 'KH',
    'russia': 'RU',
}

def get_country_code(country_name):
    # Convert country name to ISO-2 code
    if not country_name:
        return None
    
    country_lower = country_name.lower().strip()
    
    # Direct mapping
    if country_lower in COUNTRY_MAPPINGS:
        return COUNTRY_MAPPINGS[country_lower]
    
    # Check if already ISO-2 code (2 uppercase letters)
    if len(country_name) == 2 and country_name.isupper():
        return country_name
    
    # Return as-is if not found (SQL will handle validation)
    return country_name.upper()
