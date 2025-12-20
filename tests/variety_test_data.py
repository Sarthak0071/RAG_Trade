# Additional 60 diverse test questions for comprehensive SQL testing

ADDITIONAL_VARIETY_CASES = [
    # Multi-year analysis (10 questions)
    {
        "question": "Total trade value across all years?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade GROUP BY Year ORDER BY Year;",
        "category": "multi_year"
    },
    {
        "question": "Which year had highest imports?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Direction = 'I' GROUP BY Year ORDER BY SUM(Value) DESC LIMIT 1;",
        "category": "multi_year"
    },
    {
        "question": "Compare exports in 2077 and 2082?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Direction = 'E' AND Year IN (2077, 2082) GROUP BY Year;",
        "category": "multi_year"
    },
    {
        "question": "Average trade per year?",
        "expected_sql": "SELECT Year, AVG(Value) FROM trade GROUP BY Year ORDER BY Year;",
        "category": "multi_year"
    },
    {
        "question": "Total records per year?",
        "expected_sql": "SELECT Year, COUNT(*) FROM trade GROUP BY Year ORDER BY Year;",
        "category": "multi_year"
    },
    {
        "question": "Year with most export destinations?",
        "expected_sql": "SELECT Year, COUNT(DISTINCT Country) FROM trade WHERE Direction = 'E' GROUP BY Year ORDER BY COUNT(DISTINCT Country) DESC LIMIT 1;",
        "category": "multi_year"
    },
    {
        "question": "Imports from India year by year?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Country = 'IN' AND Direction = 'I' GROUP BY Year ORDER BY Year;",
        "category": "multi_year"
    },
    {
        "question": "Which year had least trade activity?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade GROUP BY Year ORDER BY SUM(Value) ASC LIMIT 1;",
        "category": "multi_year"
    },
    {
        "question": "Export growth from 2080 to 2081?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Direction = 'E' AND Year IN (2080, 2081) GROUP BY Year;",
        "category": "multi_year"
    },
    {
        "question": "All years with data?",
        "expected_sql": "SELECT DISTINCT Year FROM trade ORDER BY Year;",
        "category": "multi_year"
    },
    
    # Specific HS codes (8 questions)
    {
        "question": "Trade value of HS code 27101930?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE HS_Code = 27101930;",
        "category": "hs_code"
    },
    {
        "question": "Top 10 HS codes by value?",
        "expected_sql": "SELECT HS_Code, SUM(Value) FROM trade GROUP BY HS_Code ORDER BY SUM(Value) DESC LIMIT 10;",
        "category": "hs_code"
    },
    {
        "question": "How many unique HS codes?",
        "expected_sql": "SELECT COUNT(DISTINCT HS_Code) FROM trade;",
        "category": "hs_code"
    },
    {
        "question": "HS codes imported from China?",
        "expected_sql": "SELECT DISTINCT HS_Code FROM trade WHERE Country = 'CN' AND Direction = 'I';",
        "category": "hs_code"
    },
    {
        "question": "Most imported HS code in 2081?",
        "expected_sql": "SELECT HS_Code, SUM(Value) FROM trade WHERE Direction = 'I' AND Year = 2081 GROUP BY HS_Code ORDER BY SUM(Value) DESC LIMIT 1;",
        "category": "hs_code"
    },
    {
        "question": "HS code with highest revenue?",
        "expected_sql": "SELECT HS_Code, SUM(Revenue) FROM trade WHERE Direction = 'I' GROUP BY HS_Code ORDER BY SUM(Revenue) DESC LIMIT 1;",
        "category": "hs_code"
    },
    {
        "question": "HS codes exported to USA?",
        "expected_sql": "SELECT COUNT(DISTINCT HS_Code) FROM trade WHERE Country = 'US' AND Direction = 'E';",
        "category": "hs_code"
    },
    {
        "question": "HS code 15071000 imports?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE HS_Code = 15071000 AND Direction = 'I';",
        "category": "hs_code"
    },
    
    # Unit and Quantity based (8 questions)
    {
        "question": "What units are used for measurement?",
        "expected_sql": "SELECT DISTINCT Unit FROM trade;",
        "category": "units"
    },
    {
        "question": "Total quantity in kg?",
        "expected_sql": "SELECT SUM(Quantity) FROM trade WHERE Unit LIKE '%kg%';",
        "category": "units"
    },
    {
        "question": "Trade measured in liters?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Unit LIKE '%ltr%' OR Unit LIKE '%lit%';",
        "category": "units"
    },
    {
        "question": "Average quantity per transaction?",
        "expected_sql": "SELECT AVG(Quantity) FROM trade;",
        "category": "units"
    },
    {
        "question": "Highest single quantity imported?",
        "expected_sql": "SELECT MAX(Quantity) FROM trade WHERE Direction = 'I';",
        "category": "units"
    },
    {
        "question": "Records with zero quantity?",
        "expected_sql": "SELECT COUNT(*) FROM trade WHERE Quantity = 0;",
        "category": "units"
    },
    {
        "question": "Total quantity exported to India?",
        "expected_sql": "SELECT SUM(Quantity) FROM trade WHERE Country = 'IN' AND Direction = 'E';",
        "category": "units"
    },
    {
        "question": "Minimum quantity in any trade?",
        "expected_sql": "SELECT MIN(Quantity) FROM trade WHERE Quantity > 0;",
        "category": "units"
    },
    
    # Seasonal/Monthly patterns (8 questions)
    {
        "question": "Which month has highest trade?",
        "expected_sql": "SELECT Month, SUM(Value) FROM trade GROUP BY Month ORDER BY SUM(Value) DESC LIMIT 1;",
        "category": "seasonal"
    },
    {
        "question": "Imports in first quarter (months 1-3)?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Direction = 'I' AND Month IN (1, 2, 3);",
        "category": "seasonal"
    },
    {
        "question": "Last quarter exports?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Direction = 'E' AND Month IN (10, 11, 12);",
        "category": "seasonal"
    },
    {
        "question": "Trade by month in 2080?",
        "expected_sql": "SELECT Month, SUM(Value) FROM trade WHERE Year = 2080 GROUP BY Month ORDER BY Month;",
        "category": "seasonal"
    },
    {
        "question": "Month with least imports?",
        "expected_sql": "SELECT Month, SUM(Value) FROM trade WHERE Direction = 'I' GROUP BY Month ORDER BY SUM(Value) ASC LIMIT 1;",
        "category": "seasonal"
    },
    {
        "question": "Mid-year trade (months 5-8)?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Month BETWEEN 5 AND 8;",
        "category": "seasonal"
    },
    {
        "question": "Exports in month 12 across all years?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Month = 12 AND Direction = 'E' GROUP BY Year;",
        "category": "seasonal"
    },
    {
        "question": "Average monthly trade value?",
        "expected_sql": "SELECT Month, AVG(Value) FROM trade GROUP BY Month ORDER BY Month;",
        "category": "seasonal"
    },
    
    # Country diversity (10 questions)
    {
        "question": "Countries we export to?",
        "expected_sql": "SELECT DISTINCT Country FROM trade WHERE Direction = 'E';",
        "category": "country"
    },
    {
        "question": "Trade with South Asian countries (IN, BD, PK)?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Country IN ('IN', 'BD', 'PK') GROUP BY Country;",
        "category": "country"
    },
    {
        "question": "European countries we import from?",
        "expected_sql": "SELECT DISTINCT Country FROM trade WHERE Country IN ('DE', 'FR', 'UK', 'IT', 'ES', 'NL', 'PL') AND Direction = 'I';",
        "category": "country"
    },
    {
        "question": "Top 3 import partners?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Direction = 'I' GROUP BY Country ORDER BY SUM(Value) DESC LIMIT 3;",
        "category": "country"
    },
    {
        "question": "Countries with over 1 billion in trade?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade GROUP BY Country HAVING SUM(Value) > 1000000000;",
        "category": "country"
    },
    {
        "question": "Trade with Japan vs South Korea?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Country IN ('JP', 'KR') GROUP BY Country;",
        "category": "country"
    },
    {
        "question": "Countries we only import from?",
        "expected_sql": "SELECT DISTINCT Country FROM trade WHERE Direction = 'I' AND Country NOT IN (SELECT DISTINCT Country FROM trade WHERE Direction = 'E');",
        "category": "country"
    },
    {
        "question": "ASEAN countries trade?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Country IN ('TH', 'MY', 'SG', 'ID', 'VN', 'PH') GROUP BY Country;",
        "category": "country"
    },
    {
        "question": "Middle East imports?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country IN ('AE', 'SA', 'QA', 'KW', 'OM') AND Direction = 'I';",
        "category": "country"
    },
    {
        "question": "Countries starting with 'C'?",
        "expected_sql": "SELECT DISTINCT Country FROM trade WHERE Country LIKE 'C%';",
        "category": "country"
    },
    
    # Value ranges and thresholds (8 questions)
    {
        "question": "Trades above 1 million?",
        "expected_sql": "SELECT COUNT(*) FROM trade WHERE Value > 1000000;",
        "category": "threshold"
    },
    {
        "question": "Small trades under 1000?",
        "expected_sql": "SELECT COUNT(*) FROM trade WHERE Value < 1000;",
        "category": "threshold"
    },
    {
        "question": "Average value of large imports (>5M)?",
        "expected_sql": "SELECT AVG(Value) FROM trade WHERE Direction = 'I' AND Value > 5000000;",
        "category": "threshold"
    },
    {
        "question": "Highest single trade value?",
        "expected_sql": "SELECT MAX(Value) FROM trade;",
        "category": "threshold"
    },
    {
        "question": "Lowest non-zero trade?",
        "expected_sql": "SELECT MIN(Value) FROM trade WHERE Value > 0;",
        "category": "threshold"
    },
    {
        "question": "Medium-sized trades (100K-1M)?",
        "expected_sql": "SELECT COUNT(*) FROM trade WHERE Value BETWEEN 100000 AND 1000000;",
        "category": "threshold"
    },
    {
        "question": "Total of trades over 10M?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Value > 10000000;",
        "category": "threshold"
    },
    {
        "question": "Exports valued under 10K?",
        "expected_sql": "SELECT COUNT(*) FROM trade WHERE Direction = 'E' AND Value < 10000;",
        "category": "threshold"
    },
    
    # Edge cases and special queries (8 questions)
    {
        "question": "Records with null or zero values?",
        "expected_sql": "SELECT COUNT(*) FROM trade WHERE Value IS NULL OR Value = 0;",
        "category": "edge"
    },
    {
        "question": "Sample 100 random trades?",
        "expected_sql": "SELECT * FROM trade LIMIT 100;",
        "category": "edge"
    },
    {
        "question": "Total rows in database?",
        "expected_sql": "SELECT COUNT(*) FROM trade;",
        "category": "edge"
    },
    {
        "question": "Distinct country-year combinations?",
        "expected_sql": "SELECT COUNT(DISTINCT Year || Country) FROM trade;",
        "category": "edge"
    },
    {
        "question": "Trade records per direction?",
        "expected_sql": "SELECT Direction, COUNT(*) FROM trade GROUP BY Direction;",
        "category": "edge"
    },
    {
        "question": "Years with complete 12 months data?",
        "expected_sql": "SELECT Year, COUNT(DISTINCT Month) FROM trade GROUP BY Year HAVING COUNT(DISTINCT Month) = 12;",
        "category": "edge"
    },
    {
        "question": "Average trade value overall?",
        "expected_sql": "SELECT AVG(Value) FROM trade;",
        "category": "edge"
    },
    {
        "question": "Median trade value approximation?",
        "expected_sql": "SELECT AVG(Value) FROM (SELECT Value FROM trade ORDER BY Value LIMIT 2 OFFSET (SELECT COUNT(*)/2 FROM trade));",
        "category": "edge"
    }
]

# Total: 60 additional diverse questions
