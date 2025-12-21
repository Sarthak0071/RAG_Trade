"""
SQL query executor with intelligent error recovery.

Features:
- Pre-execution validation
- Safe DuckDB execution
- Automatic regeneration on failure
- Timeout handling with LIMIT injection
- Comprehensive failure logging
- Result capture as DataFrame
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional, Callable

from src.database import TradeDatabase
from src.validators import SQLValidator


class QueryExecutor:
    """Execute SQL queries with intelligent error recovery."""
    
    def __init__(self, max_retries: int = 2, log_failures: bool = True):
        """
        Initialize executor.
        
        Args:
            max_retries: Maximum retry attempts
            log_failures: Whether to log failures to file
        """
        self.validator = SQLValidator()
        self.max_retries = max_retries
        self.log_failures = log_failures
        self.log_file = Path("logs/query_errors.jsonl")
        
        if self.log_failures:
            self.log_file.parent.mkdir(exist_ok=True)
    
    def execute(
        self,
        sql: str,
        question: str = "",
        regenerate_fn: Optional[Callable[[str], str]] = None
    ) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Execute SQL with full error recovery pipeline.
        
        Args:
            sql: SQL query to execute
            question: Original question (for regeneration)
            regenerate_fn: Function to regenerate SQL on failure
            
        Returns:
            (success, dataframe, message)
        """
        # Validate
        is_valid, error_msg = self.validator.validate(sql)
        if not is_valid:
            if regenerate_fn and question:
                return self._try_regenerate(question, regenerate_fn, f"Validation error: {error_msg}")
            return False, None, f"Validation failed: {error_msg}"
        
        # Extract clean SQL
        clean_sql = self.validator.extract_sql(sql)
        
        # Execute with retry
        for attempt in range(self.max_retries + 1):
            try:
                with TradeDatabase() as db:
                    result = db.execute_query(clean_sql)
                    
                    if result.empty:
                        return True, result, "No data found"
                    
                    return True, result, f"Success: {len(result)} rows"
                    
            except Exception as e:
                error_str = str(e)
                
                # Timeout - add LIMIT
                if "timeout" in error_str.lower() and attempt < self.max_retries:
                    clean_sql = self._add_limit(clean_sql, 1000)
                    continue
                
                # Syntax error - try regenerate
                if ("syntax error" in error_str.lower() or "parser error" in error_str.lower()):
                    if regenerate_fn and question and attempt == 0:
                        return self._try_regenerate(question, regenerate_fn, error_str)
                
                # Final failure
                if attempt == self.max_retries:
                    self._log_failure(question, clean_sql, error_str)
                    return False, None, f"Execution failed: {error_str}"
        
        return False, None, "Unknown error"
    
    def _try_regenerate(
        self,
        question: str,
        regenerate_fn: Callable[[str], str],
        original_error: str
    ) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Attempt to regenerate SQL and execute.
        
        Args:
            question: Original question
            regenerate_fn: Regeneration function
            original_error: Error from first attempt
            
        Returns:
            (success, dataframe, message)
        """
        print(f"    → Regenerating SQL (reason: {original_error[:50]}...)")
        
        try:
            new_sql = regenerate_fn(question)
            
            # Validate new SQL
            is_valid, error_msg = self.validator.validate(new_sql)
            if not is_valid:
                self._log_failure(question, new_sql, f"Regenerated SQL invalid: {error_msg}")
                return False, None, f"Regeneration failed validation: {error_msg}"
            
            # Execute new SQL (no regeneration on second attempt)
            clean_sql = self.validator.extract_sql(new_sql)
            
            with TradeDatabase() as db:
                result = db.execute_query(clean_sql)
                
                if result.empty:
                    return True, result, "Regenerated: No data found"
                
                return True, result, f"Regenerated: Success ({len(result)} rows)"
                
        except Exception as e:
            error_str = str(e)
            self._log_failure(question, new_sql if 'new_sql' in locals() else "N/A", f"Regeneration failed: {error_str}")
            return False, None, f"Regeneration execution failed: {error_str}"
    
    def _add_limit(self, sql: str, limit: int = 1000) -> str:
        """
        Add LIMIT clause to prevent timeout.
        
        Args:
            sql: Original SQL
            limit: Row limit
            
        Returns:
            SQL with LIMIT
        """
        sql_upper = sql.upper()
        
        if "LIMIT" in sql_upper:
            return sql
        
        if sql.strip().endswith(';'):
            return sql.rstrip(';').strip() + f" LIMIT {limit};"
        else:
            return sql.strip() + f" LIMIT {limit}"
    
    def _log_failure(self, question: str, sql: str, error: str):
        """
        Log failure to JSONL file.
        
        Args:
            question: Original question
            sql: Failed SQL
            error: Error message
        """
        if not self.log_failures:
            return
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "sql": sql,
            "error": error
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
