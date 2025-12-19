# Trade Data RAG System

## Overview
Smart question-answering system for Nepal trade data using local LLMs.

**Target:** 90% accuracy, 3-second response time

## Architecture
- **SQL Generator:** Mistral-7B (4-bit) - Natural language → SQL
- **Database:** DuckDB - Fast query execution on done_des.csv
- **Formatter:** Llama-3.2-1B (4-bit) - Results → Natural language
- **GPU:** RTX 4060 (6GB) - Accelerated inference

## Project Structure
```
rag_system/
├── src/                    # Core source code
├── tests/                  # pytest test suite
├── prompts/                # Prompt templates
├── logs/                   # Query logs
├── data/                   # DuckDB database
├── config/                 # Configuration
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run
```bash
python run.py
```

## Development Phases
1. Setup - Install dependencies, load models
2. SQL Generation - Comprehensive prompt engineering
3. Execution - Safe query execution with validation
4. Formatting - Clear responses with exact numbers
5. Testing - 50+ test cases for 90% accuracy

## Testing
```bash
pytest tests/ -v
```

## Performance
- Response time: ~3 seconds (GPU)
- Accuracy: 90%+ on test suite
- Data: 760,233 trade records

## License
Internal use only
