# Test cases for SQL generation accuracy

# Total: 90 test cases (50 basic + 40 detailed trade-specific)

TEST_CASES = [
    # Basic aggregation (5 cases)
    {
        "question": "What is the total trade value?",
        "expected_sql": "SELECT SUM(Value) FROM trade;",
        "category": "basic"
    },
    {
        "question": "Total imports?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Direction = 'I';",
        "category": "basic"
    },
    {
        "question": "Total exports?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Direction = 'E';",
        "category": "basic"
    },
    {
        "question": "How many trade records?",
        "expected_sql": "SELECT COUNT(*) FROM trade;",
        "category": "basic"
    },
    {
        "question": "Average trade value?",
        "expected_sql": "SELECT AVG(Value) FROM trade;",
        "category": "basic"
    },
    
    # Year filtering (5 cases)
    {
        "question": "Total trade in 2080?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Year = 2080;",
        "category": "year_filter"
    },
    {
        "question": "Imports in 2081?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Year = 2081 AND Direction = 'I';",
        "category": "year_filter"
    },
    {
        "question": "Exports in 2082?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Year = 2082 AND Direction = 'E';",
        "category": "year_filter"
    },
    {
        "question": "Trade records in 2079?",
        "expected_sql": "SELECT COUNT(*) FROM trade WHERE Year = 2079;",
        "category": "year_filter"
    },
    {
        "question": "Average import value in 2080?",
        "expected_sql": "SELECT AVG(Value) FROM trade WHERE Year = 2080 AND Direction = 'I';",
        "category": "year_filter"
    },
    
    # Country filtering (10 cases)
    {
        "question": "Trade with India?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'IN';",
        "category": "country_filter"
    },
    {
        "question": "Imports from China?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'CN' AND Direction = 'I';",
        "category": "country_filter"
    },
    {
        "question": "Exports to USA?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'US' AND Direction = 'E';",
        "category": "country_filter"
    },
    {
        "question": "Trade with Japan?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'JP';",
        "category": "country_filter"
    },
    {
        "question": "Imports from Germany?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'DE' AND Direction = 'I';",
        "category": "country_filter"
    },
    {
        "question": "Trade with Thailand in 2081?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'TH' AND Year = 2081;",
        "category": "country_filter"
    },
    {
        "question": "Exports to Malaysia?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'MY' AND Direction = 'E';",
        "category": "country_filter"
    },
    {
        "question": "Imports from Bangladesh?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'BD' AND Direction = 'I';",
        "category": "country_filter"
    },
    {
        "question": "Trade with UAE?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'AE';",
        "category": "country_filter"
    },
    {
        "question": "Imports from India in 2080?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'IN' AND Direction = 'I' AND Year = 2080;",
        "category": "country_filter"
    },
    
    # Commodity filtering (8 cases)
    {
        "question": "How much wheat was imported?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%wheat%' AND Direction = 'I';",
        "category": "commodity"
    },
    {
        "question": "Rice imports?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%rice%' AND Direction = 'I';",
        "category": "commodity"
    },
    {
        "question": "Sugar exports?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%sugar%' AND Direction = 'E';",
        "category": "commodity"
    },
    {
        "question": "Trade value of oil?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%oil%';",
        "category": "commodity"
    },
    {
        "question": "Wheat from India?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%wheat%' AND Country = 'IN';",
        "category": "commodity"
    },
    {
        "question": "Rice imports in 2081?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%rice%' AND Direction = 'I' AND Year = 2081;",
        "category": "commodity"
    },
    {
        "question": "Quantity of wheat imported?",
        "expected_sql": "SELECT SUM(Quantity) FROM trade WHERE Description LIKE '%wheat%' AND Direction = 'I';",
        "category": "commodity"
    },
    {
        "question": "Iron imports from China?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%iron%' AND Country = 'CN' AND Direction = 'I';",
        "category": "commodity"
    },
    
    # GROUP BY queries (10 cases)
    {
        "question": "Trade value by year?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade GROUP BY Year ORDER BY Year;",
        "category": "groupby"
    },
    {
        "question": "Monthly imports in 2081?",
        "expected_sql": "SELECT Month, SUM(Value) FROM trade WHERE Year = 2081 AND Direction = 'I' GROUP BY Month ORDER BY Month;",
        "category": "groupby"
    },
    {
        "question": "Top 10 import countries?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Direction = 'I' GROUP BY Country ORDER BY SUM(Value) DESC LIMIT 10;",
        "category": "groupby"
    },
    {
        "question": "Imports vs exports by year?",
        "expected_sql": "SELECT Year, Direction, SUM(Value) FROM trade GROUP BY Year, Direction ORDER BY Year;",
        "category": "groupby"
    },
    {
        "question": "Top 5 commodities by value?",
        "expected_sql": "SELECT Description, SUM(Value) FROM trade GROUP BY Description ORDER BY SUM(Value) DESC LIMIT 5;",
        "category": "groupby"
    },
    {
        "question": "Trade by month?",
        "expected_sql": "SELECT Month, SUM(Value) FROM trade GROUP BY Month ORDER BY Month;",
        "category": "groupby"
    },
    {
        "question": "Top export destinations?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Direction = 'E' GROUP BY Country ORDER BY SUM(Value) DESC LIMIT 10;",
        "category": "groupby"
    },
    {
        "question": "Import value by country in 2080?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Year = 2080 AND Direction = 'I' GROUP BY Country ORDER BY SUM(Value) DESC;",
        "category": "groupby"
    },
    {
        "question": "Monthly export trend in 2082?",
        "expected_sql": "SELECT Month, SUM(Value) FROM trade WHERE Year = 2082 AND Direction = 'E' GROUP BY Month ORDER BY Month;",
        "category": "groupby"
    },
    {
        "question": "Top HS codes?",
        "expected_sql": "SELECT HS_Code, SUM(Value) FROM trade GROUP BY HS_Code ORDER BY SUM(Value) DESC LIMIT 10;",
        "category": "groupby"
    },
    
    # Complex queries (12 cases)
    {
        "question": "How many countries do we trade with?",
        "expected_sql": "SELECT COUNT(DISTINCT Country) FROM trade;",
        "category": "complex"
    },
    {
        "question": "Total import revenue in 2081?",
        "expected_sql": "SELECT SUM(Revenue) FROM trade WHERE Year = 2081 AND Direction = 'I';",
        "category": "complex"
    },
    {
        "question": "Compare imports and exports?",
        "expected_sql": "SELECT Direction, SUM(Value) FROM trade GROUP BY Direction;",
        "category": "complex"
    },
    {
        "question": "Trade between 2080 and 2082?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Year BETWEEN 2080 AND 2082;",
        "category": "complex"
    },
    {
        "question": "Exports to China and USA?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Direction = 'E' AND Country IN ('CN', 'US') GROUP BY Country;",
        "category": "complex"
    },
    {
        "question": "Average monthly import value?",
        "expected_sql": "SELECT AVG(monthly_total) FROM (SELECT Month, SUM(Value) AS monthly_total FROM trade WHERE Direction = 'I' GROUP BY Month);",
        "category": "complex"
    },
    {
        "question": "Unique commodities traded?",
        "expected_sql": "SELECT COUNT(DISTINCT Description) FROM trade;",
        "category": "complex"
    },
    {
        "question": "Trade with India, China, and USA?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Country IN ('IN', 'CN', 'US') GROUP BY Country;",
        "category": "complex"
    },
    {
        "question": "Imports in month 4?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Month = 4 AND Direction = 'I';",
        "category": "complex"
    },
    {
        "question": "Total quantity imported?",
        "expected_sql": "SELECT SUM(Quantity) FROM trade WHERE Direction = 'I';",
        "category": "complex"
    },
    {
        "question": "Trade records for HS code 10019100?",
        "expected_sql": "SELECT * FROM trade WHERE HS_Code = 10019100 LIMIT 100;",
        "category": "complex"
    },
    {
        "question": "Years with data?",
        "expected_sql": "SELECT DISTINCT Year FROM trade ORDER BY Year;",
        "category": "complex"
    }
]

# Detailed trade-specific questions (40 cases) - DIRECTLY INCLUDED
# Month-specific queries
TEST_CASES.extend([
    {
        "question": "What are the total wheat imports from China in month 6 of 2082?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Month = 6 AND Year = 2082 AND Country = 'CN' AND Direction = 'I' AND Description LIKE '%wheat%';",
        "category": "month_specific"
    },
    {
        "question": "Rice exports to India in Shrawan 2081?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%rice%' AND Country = 'IN' AND Direction = 'E' AND Month = 4 AND Year = 2081;",
        "category": "month_specific"
    },
    {
        "question": "Total imports in Baishakh month?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Direction = 'I' AND Month = 1;",
        "category": "month_specific"
    },
    {
        "question": "Trade with India in Chaitra 2080?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'IN' AND Month = 12 AND Year = 2080;",
        "category": "month_specific"
    },
    {
        "question": "Oil imports in Kartik month?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%oil%' AND Direction = 'I' AND Month = 7;",
        "category": "month_specific"
    },
    # Commodity-country combinations
    {
        "question": "Steel imports from China?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%steel%' AND Country = 'CN' AND Direction = 'I';",
        "category": "commodity_country"
    },
    {
        "question": "Tea exports to USA?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%tea%' AND Country = 'US' AND Direction = 'E';",
        "category": "commodity_country"
    },
    {
        "question": "Total copper imports from India?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%copper%' AND Country = 'IN' AND Direction = 'I';",
        "category": "commodity_country"
    },
    {
        "question": "Gold imports from UAE?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%gold%' AND Country = 'AE' AND Direction = 'I';",
        "category": "commodity_country"
    },
    {
        "question": "Textile exports to Germany?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Description LIKE '%textile%' AND Country = 'DE' AND Direction = 'E';",
        "category": "commodity_country"
    },
    # Quantity-based queries
    {
        "question": "Total quantity of rice imported?",
        "expected_sql": "SELECT SUM(Quantity) FROM trade WHERE Description LIKE '%rice%' AND Direction = 'I';",
        "category": "quantity"
    },
    {
        "question": "Wheat quantity from India in 2081?",
        "expected_sql": "SELECT SUM(Quantity) FROM trade WHERE Description LIKE '%wheat%' AND Country = 'IN' AND Year = 2081;",
        "category": "quantity"
    },
    {
        "question": "Oil quantity imported in 2082?",
        "expected_sql": "SELECT SUM(Quantity) FROM trade WHERE Description LIKE '%oil%' AND Direction = 'I' AND Year = 2082;",
        "category": "quantity"
    },
    {
        "question": "Total export quantity to China?",
        "expected_sql": "SELECT SUM(Quantity) FROM trade WHERE Country = 'CN' AND Direction = 'E';",
        "category": "quantity"
    },
    {
        "question": "Average quantity per import transaction?",
        "expected_sql": "SELECT AVG(Quantity) FROM trade WHERE Direction = 'I';",
        "category": "quantity"
    },
    # Year comparisons
    {
        "question": "Trade with India in 2082?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE Country = 'IN' AND Year = 2082;",
        "category": "year_comparison"
    },
    {
        "question": "Imports trend from 2077 to 2082?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Direction = 'I' GROUP BY Year ORDER BY Year;",
        "category": "year_comparison"
    },
    {
        "question": "Wheat imports growth by year?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Description LIKE '%wheat%' AND Direction = 'I' GROUP BY Year ORDER BY Year;",
        "category": "year_comparison"
    },
    {
        "question": "China trade by year?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Country = 'CN' GROUP BY Year ORDER BY Year;",
        "category": "year_comparison"
    },
    {
        "question": "Export trend to USA by year?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Country = 'US' AND Direction = 'E' GROUP BY Year ORDER BY Year;",
        "category": "year_comparison"
    },
    # Revenue queries
    {
        "question": "Total import revenue from India?",
        "expected_sql": "SELECT SUM(Revenue) FROM trade WHERE Country = 'IN' AND Direction = 'I';",
        "category": "revenue"
    },
    {
        "question": "Revenue from wheat imports?",
        "expected_sql": "SELECT SUM(Revenue) FROM trade WHERE Description LIKE '%wheat%' AND Direction = 'I';",
        "category": "revenue"
    },
    {
        "question": "Import revenue in 2080?",
        "expected_sql": "SELECT SUM(Revenue) FROM trade WHERE Year = 2080 AND Direction = 'I';",
        "category": "revenue"
    },
    {
        "question": "Revenue from China imports in 2082?",
        "expected_sql": "SELECT SUM(Revenue) FROM trade WHERE Country = 'CN' AND Direction = 'I' AND Year = 2082;",
        "category": "revenue"
    },
    {
        "question": "Average revenue per import?",
        "expected_sql": "SELECT AVG(Revenue) FROM trade WHERE Direction = 'I';",
        "category": "revenue"
    },
    # Top N queries
    {
        "question": "Top 5 wheat importing countries?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Description LIKE '%wheat%' AND Direction = 'I' GROUP BY Country ORDER BY SUM(Value) DESC LIMIT 5;",
        "category": "top_n"
    },
    {
        "question": "Top 3 commodities from India?",
        "expected_sql": "SELECT Description, SUM(Value) FROM trade WHERE Country = 'IN' GROUP BY Description ORDER BY SUM(Value) DESC LIMIT 3;",
        "category": "top_n"
    },
    {
        "question": "Top 10 months for imports?",
        "expected_sql": "SELECT Month, SUM(Value) FROM trade WHERE Direction = 'I' GROUP BY Month ORDER BY SUM(Value) DESC LIMIT 10;",
        "category": "top_n"
    },
    {
        "question": "Top 5 export years?",
        "expected_sql": "SELECT Year, SUM(Value) FROM trade WHERE Direction = 'E' GROUP BY Year ORDER BY SUM(Value) DESC LIMIT 5;",
        "category": "top_n"
    },
    {
        "question": "Least traded commodities?",
        "expected_sql": "SELECT Description, SUM(Value) FROM trade GROUP BY Description ORDER BY SUM(Value) ASC LIMIT 10;",
        "category": "top_n"
    },
    # Direction-specific
    {
        "question": "What percentage of trade is imports?",
        "expected_sql": "SELECT (SUM(CASE WHEN Direction = 'I' THEN Value ELSE 0 END) * 100.0 / SUM(Value)) FROM trade;",
        "category": "percentage"
    },
    {
        "question": "Import-export ratio for India?",
        "expected_sql": "SELECT Direction, SUM(Value) FROM trade WHERE Country = 'IN' GROUP BY Direction;",
        "category": "ratio"
    },
    {
        "question": "Which country has highest import value?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Direction = 'I' GROUP BY Country ORDER BY SUM(Value) DESC LIMIT 1;",
        "category": "highest"
    },
    {
        "question": "Which commodity is exported most?",
        "expected_sql": "SELECT Description, SUM(Value) FROM trade WHERE Direction = 'E' GROUP BY Description ORDER BY SUM(Value) DESC LIMIT 1;",
        "category": "highest"
    },
    {
        "question": "Busiest month for trade?",
        "expected_sql": "SELECT Month, SUM(Value) FROM trade GROUP BY Month ORDER BY SUM(Value) DESC LIMIT 1;",
        "category": "highest"
    },
    # Multiple conditions
    {
        "question": "Wheat and rice imports from India?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE (Description LIKE '%wheat%' OR Description LIKE '%rice%') AND Country = 'IN' AND Direction = 'I';",
        "category": "multiple_conditions"
    },
    {
        "question": "Trade with India or China in 2081?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Country IN ('IN', 'CN') AND Year = 2081 GROUP BY Country;",
        "category": "multiple_conditions"
    },
    {
        "question": "Imports or exports above 10 million?",
        "expected_sql": "SELECT * FROM trade WHERE Value > 10000000 LIMIT 100;",
        "category": "multiple_conditions"
    },
    {
        "question": "Oil or gas imports?",
        "expected_sql": "SELECT SUM(Value) FROM trade WHERE (Description LIKE '%oil%' OR Description LIKE '%gas%') AND Direction = 'I';",
        "category": "multiple_conditions"
    },
    {
        "question": "China and USA export destinations?",
        "expected_sql": "SELECT Country, SUM(Value) FROM trade WHERE Country IN ('CN', 'US') AND Direction = 'E' GROUP BY Country;",
        "category": "multiple_conditions"
    }
])

# Import and add 60 variety questions
from tests.variety_test_data import ADDITIONAL_VARIETY_CASES
TEST_CASES.extend(ADDITIONAL_VARIETY_CASES)

# Total: 150 test cases (90 core + 60 variety)
