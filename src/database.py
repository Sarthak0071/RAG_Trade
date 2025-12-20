# DuckDB database operations for trade data

import duckdb
import pandas as pd
from pathlib import Path
from typing import Optional
from config.settings import DATA_CSV_PATH, DUCKDB_PATH, TABLE_NAME, MAX_QUERY_TIMEOUT

class TradeDatabase:
    # Manages DuckDB connection and query execution for trade data
    
    def __init__(self):
        self.conn = duckdb.connect(DUCKDB_PATH)
        self.table_loaded = False
    
    def load_data(self) -> None:
        # Load done_des.csv into DuckDB table
        if self.table_loaded:
            return
        
        csv_path = str(DATA_CSV_PATH)
        
        self.conn.execute(f"""
            CREATE TABLE {TABLE_NAME} AS 
            SELECT * FROM read_csv_auto('{csv_path}')
        """)
        
        self.table_loaded = True
    
    def execute_query(self, sql: str, timeout: int = MAX_QUERY_TIMEOUT) -> Optional[pd.DataFrame]:
        # Execute SQL query and return DataFrame
        try:
            result = self.conn.execute(sql).fetchdf()
            return result
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")
    
    def get_row_count(self) -> int:
        # Get total number of rows in trade table
        result = self.conn.execute(f"SELECT COUNT(*) as count FROM {TABLE_NAME}").fetchone()
        return result[0] if result else 0
    
    def get_schema(self) -> pd.DataFrame:
        # Return table schema information
        return self.conn.execute(f"DESCRIBE {TABLE_NAME}").fetchdf()
    
    def close(self) -> None:
        # Close database connection
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        self.load_data()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

