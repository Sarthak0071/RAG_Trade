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
# RAG system configuration

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
MODELS_DIR = BASE_DIR / "models"

# Data
DATA_CSV_PATH = DATA_DIR / "done_des.csv"
DUCKDB_PATH = ":memory:"
TABLE_NAME = "trade"

# Model configurations
MISTRAL_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
LLAMA_MODEL = "meta-llama/Llama-3.2-1B-Instruct"

# Quantization settings
LOAD_IN_4BIT = True
DEVICE_MAP = "auto"  # Automatically use GPU

# Model settings
SQL_MAX_TOKENS = 256
FORMAT_MAX_TOKENS = 512
SQL_TEMPERATURE = 0.0  # Deterministic for SQL generation
FORMAT_TEMPERATURE = 0.7  # Creative for natural responses
TEMPERATURE = 0.7  # Legacy, use SQL_TEMPERATURE or FORMAT_TEMPERATURE

# Query settings
MAX_QUERY_TIMEOUT = 30
DEFAULT_LIMIT = 1000

# Logging
LOG_QUERIES = True
LOG_ERRORS = True
LOG_PERFORMANCE = True

# Create directories
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
