"""
Configuration settings for RAG system
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# Data source
DATA_CSV_PATH = PROJECT_ROOT.parent / "done_des.csv"

# Model configurations
MISTRAL_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
LLAMA_MODEL = "meta-llama/Llama-3.2-1B-Instruct"

# Quantization settings
LOAD_IN_4BIT = True
DEVICE_MAP = "auto"  # Automatically use GPU

# Database settings
DUCKDB_PATH = ":memory:"  # In-memory database
TABLE_NAME = "trade"

# Generation settings
SQL_MAX_TOKENS = 200
FORMAT_MAX_TOKENS = 150
TEMPERATURE = 0  # Deterministic for consistency

# Query settings
MAX_QUERY_TIMEOUT = 30  # seconds
DEFAULT_LIMIT = 1000  # Default row limit for safety

# Logging
LOG_QUERIES = True
LOG_ERRORS = True
LOG_PERFORMANCE = True

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)
