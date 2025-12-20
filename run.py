from src.models import ModelLoader
import sys

def main():
    print("Trade Data RAG System - Model Test\n")
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"GPU: {gpu_name} ({gpu_mem:.1f} GB)")
        else:
            print("GPU: Not available (using CPU)")
    except ImportError:
        print("GPU: PyTorch not installed (ctransformers will handle GPU)")
    
    print("\nLoading models...")
    loader = ModelLoader()
    
    try:
        print("  Loading Mistral-7B (SQL Generator)...")
        loader.load_sql_generator()
        print("  Mistral-7B loaded")
        
        print("  Loading TinyLlama (Response Formatter)...")
        loader.load_response_formatter()
        print("  TinyLlama loaded")
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Run: python scripts/download_models.py")
        sys.exit(1)
    except Exception as e:
        print(f"\nError loading models: {e}")
        sys.exit(1)
    
    # Test SQL generation
    print("\nTesting SQL Generator (Mistral-7B)")
    sql_prompt = """Generate a SQL query to get total trade value from the 'trade' table.
Table: trade
Columns: Year, Month, Direction, HS_Code, Description, Country, Value, Quantity, Unit, Revenue

SQL:"""
    
    print(f"Prompt: {sql_prompt[:100]}...")
    sql_result = loader.generate_sql(sql_prompt)
    print(f"\nGenerated SQL:\n{sql_result}\n")
    
    # Test response formatting
    print("Testing Response Formatter (TinyLlama)")
    format_prompt = """Format this data as a clear answer:
Question: What is the total trade value?
Data: 5200000

Answer in simple words:"""
    
    print(f"Prompt: {format_prompt[:100]}...")
    format_result = loader.format_response(format_prompt)
    print(f"\nFormatted Response:\n{format_result}\n")
    
    print("Both models working!")
    print("\nNext: Phase 2 - Prompt Engineering")
    print("Create comprehensive SQL prompts for 90% accuracy")

if __name__ == "__main__":
    main()

