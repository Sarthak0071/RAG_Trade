# GGUF model loading and inference using ctransformers

from ctransformers import AutoModelForCausalLM
from pathlib import Path
from typing import Optional
from config.settings import SQL_MAX_TOKENS, FORMAT_MAX_TOKENS, TEMPERATURE

class ModelLoader:
    # Manages loading and inference for GGUF quantized models
    
    def __init__(self):
        self.sql_model = None
        self.format_model = None
        self.models_dir = Path("models")
    
    def load_sql_generator(self, model_path: Optional[str] = None) -> None:
        # Load Mistral-7B GGUF model for SQL generation
        if model_path is None:
            model_path = self.models_dir / "mistral_sql" / "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        
        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}\nRun download_models.py first")
        
        print(f"Loading SQL generator from {model_path}...")
        self.sql_model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            model_type="mistral",
            gpu_layers=50,
            context_length=2048
        )
        print("SQL generator loaded")
    
    def load_response_formatter(self, model_path: Optional[str] = None) -> None:
        # Load TinyLlama GGUF model for response formatting
        if model_path is None:
            model_path = self.models_dir / "tinyllama_formatter" / "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
        
        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}\nRun download_models.py first")
        
        print(f"Loading response formatter from {model_path}...")
        self.format_model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            model_type="llama",
            gpu_layers=50,
            context_length=2048
        )
        print("Response formatter loaded")
    
    def generate_sql(self, prompt: str) -> str:
        # Generate SQL query from natural language prompt
        if not self.sql_model:
            raise RuntimeError("SQL model not loaded")
        
        response = self.sql_model(
            prompt,
            max_new_tokens=SQL_MAX_TOKENS,
            temperature=TEMPERATURE,
            stop=["\n\n", "</s>"]
        )
        
        return response.strip()
    
    def format_response(self, prompt: str) -> str:
        # Format query results into natural language response
        if not self.format_model:
            raise RuntimeError("Format model not loaded")
        
        response = self.format_model(
            prompt,
            max_new_tokens=FORMAT_MAX_TOKENS,
            temperature=TEMPERATURE,
            stop=["</s>"]
        )
        
        return response.strip()
    
    def get_memory_usage(self) -> dict:
        # Get GPU memory usage if available
        try:
            import torch
            if torch.cuda.is_available():
                return {
                    "allocated_gb": torch.cuda.memory_allocated() / 1024**3,
                    "reserved_gb": torch.cuda.memory_reserved() / 1024**3,
                }
        except:
            pass
        
        return {"note": "ctransformers manages memory automatically"}


