# SQL validation and security for safe query execution

import re
from typing import Tuple, Optional
from config.settings import TABLE_NAME, DEFAULT_LIMIT

class SQLValidator:
    # Validates and sanitizes SQL queries for security
    
    @staticmethod
    def is_select_only(sql: str) -> bool:
        # Check if query is SELECT-only (blocks INSERT, UPDATE, DELETE, etc.)
        sql_upper = sql.strip().upper()
        dangerous_keywords = [
            'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
            'TRUNCATE', 'REPLACE', 'MERGE', 'EXEC', 'EXECUTE'
        ]
        
        for keyword in dangerous_keywords:
            if re.search(rf'\b{keyword}\b', sql_upper):
                return False
        
        return sql_upper.startswith('SELECT')
    
    @staticmethod
    def targets_trade_table(sql: str) -> bool:
        # Verify query targets the 'trade' table
        sql_upper = sql.upper()
        return TABLE_NAME.upper() in sql_upper
    
    @staticmethod
    def has_limit(sql: str) -> bool:
        # Check if query has LIMIT clause
        return bool(re.search(r'\bLIMIT\s+\d+', sql, re.IGNORECASE))
    
    @staticmethod
    def add_limit_if_missing(sql: str, limit: int = DEFAULT_LIMIT) -> str:
        # Add LIMIT clause if missing for safety
        if SQLValidator.has_limit(sql):
            return sql
        
        sql = sql.strip()
        if sql.endswith(';'):
            sql = sql[:-1].strip()
        
        return f"{sql} LIMIT {limit};"
    
    @staticmethod
    def extract_sql(text: str) -> Optional[str]:
        # Extract SQL from various formats (markdown code blocks, plain text)
        patterns = [
            r'```sql\s*(.*?)\s*```',
            r'```\s*(SELECT.*?)\s*```',
            r'(SELECT\s+.*?(?:;|$))'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        if text.strip().upper().startswith('SELECT'):
            return text.strip()
        
        return None
    
    @staticmethod
    def validate(sql: str) -> Tuple[bool, str]:
        # Validate SQL query against security rules
        if not sql or not sql.strip():
            return False, "Empty SQL query"
        
        sql = sql.strip()
        
        if not SQLValidator.is_select_only(sql):
            return False, "Only SELECT queries are allowed"
        
        if not SQLValidator.targets_trade_table(sql):
            return False, f"Query must target the '{TABLE_NAME}' table"
        
        return True, "Valid"
    
    @staticmethod
    def sanitize(sql: str) -> str:
        # Sanitize SQL by adding safety measures
        sql = sql.strip()
        sql = SQLValidator.add_limit_if_missing(sql)
        return sql

