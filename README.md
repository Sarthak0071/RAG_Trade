# Trade Data RAG System

Natural language query system for Nepal trade data.

## Setup

```bash
pip install -r requirements.txt
pip install ctransformers[cuda]
python scripts/download_models.py
```

## Run

```bash
python run.py
```

## Architecture

- Mistral-7B (SQL generation)
- TinyLlama-1.1B (response formatting)
- DuckDB (760K trade records)

## Structure

```
rag_system/
├── models/           # Downloaded models
├── tests/            # Test suite
└── run.py            # Main entry
```

## Requirements

- Python 3.11
- CUDA 11.8 (for GPU)
- 6GB+ GPU memory

## Documentation

See `docs/` folder for detailed guides.


