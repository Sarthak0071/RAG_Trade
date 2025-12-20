# Structured logging for queries, errors, and performance tracking

import logging
import json
from pathlib import Path
from datetime import datetime
from config.settings import LOGS_DIR, LOG_QUERIES, LOG_ERRORS, LOG_PERFORMANCE

class RAGLogger:
    # Handles structured JSON logging for RAG system
    
    def __init__(self):
        self.queries_log = LOGS_DIR / "queries.log"
        self.errors_log = LOGS_DIR / "errors.log"
        self.performance_log = LOGS_DIR / "performance.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def log_query(self, question: str, sql: str, result_count: int, answer: str, elapsed_time: float) -> None:
        # Log query with metadata for analysis
        if not LOG_QUERIES:
            return
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "sql": sql,
            "result_count": result_count,
            "answer": answer,
            "elapsed_time": elapsed_time
        }
        
        with open(self.queries_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    
    def log_error(self, error_type: str, message: str, details: dict = None) -> None:
        # Log errors with context for debugging
        if not LOG_ERRORS:
            return
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "message": message,
            "details": details or {}
        }
        
        with open(self.errors_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
        
        self.logger.error(f"{error_type}: {message}")
    
    def log_performance(self, stage: str, elapsed_time: float, memory_usage: dict = None) -> None:
        # Log performance metrics for optimization
        if not LOG_PERFORMANCE:
            return
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "stage": stage,
            "elapsed_time": elapsed_time,
            "memory_usage": memory_usage or {}
        }
        
        with open(self.performance_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

