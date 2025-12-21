
"""
GGUF model loading and inference using ctransformers.

This module handles loading quantized GGUF models for:
- SQL generation (Mistral-7B)
- Response formatting (TinyLlama-1.1B)
"""

from ctransformers import AutoModelForCausalLM
from pathlib import Path
from typing import Optional
from config.settings import SQL_MAX_TOKENS, FORMAT_MAX_TOKENS, TEMPERATURE


class ModelLoader:
    """Manages loading and inference for GGUF quantized models."""
    
    def __init__(self):
        """Initialize model loader with empty model slots."""
        self.sql_model = None
        self.formatter_model = None
        self.models_dir = Path("models")
    
    def load_sql_generator(self) -> None:
        """
        Load Mistral-7B GGUF model for SQL generation.
        
        Raises:
            FileNotFoundError: If model file not found.
        """
        if self.sql_model is not None:
            return
        
        model_path = self.models_dir / "mistral_sql" / "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
        
        if not model_path.exists():
            raise FileNotFoundError(f"SQL model not found: {model_path}")
        
        print(f"Loading SQL generator from {model_path}...")
        
        self.sql_model = AutoModelForCausalLM.from_pretrained(
            str(model_path.parent),
            model_file=model_path.name,
            model_type="mistral",
            gpu_layers=-1,  # Use all GPU layers
            lib='cuda',  # Force CUDA backend
            context_length=1024,
            threads=8,  # Use more CPU threads
            batch_size=512,  # Larger batch for faster processing
            mlock=True  # Lock model in RAM for speed
        )
        
        print("SQL generator loaded")
    
    def load_response_formatter(self) -> None:
        """
        Load TinyLlama GGUF model for response formatting.
        
        Raises:
            FileNotFoundError: If model file not found.
        """
        if self.formatter_model is not None:
            return
        
        model_path = self.models_dir / "tinyllama_formatter" / "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Formatter model not found: {model_path}")
        
        print(f"Loading response formatter from {model_path}...")
        
        self.formatter_model = AutoModelForCausalLM.from_pretrained(
            str(model_path.parent),
            model_file=model_path.name,
            model_type="llama",
            gpu_layers=-1,  # Use all GPU layers
            lib='cuda',  # Force CUDA backend
            context_length=1024
        )
        
        print("Response formatter loaded")
    
    def generate_sql(self, prompt: str) -> str:
        """
        Generate SQL query from natural language prompt.
        
        Args:
            prompt: Natural language question with schema context.
            
        Returns:
            Generated SQL query string.
            
        Raises:
            RuntimeError: If SQL model not loaded.
        """
        if self.sql_model is None:
            raise RuntimeError("SQL model not loaded. Call load_sql_generator() first")
        
        response = self.sql_model(
            prompt,
            max_new_tokens=150,
            temperature=0.25,  # Balanced for accuracy and speed
            top_p=0.85,  # Slightly higher for better quality
            repetition_penalty=1.15,
            stop=["\n\nQuestion:", "Q:"],
            threads=8
        )
        
        return response.strip()
    
    def format_response(self, prompt: str) -> str:
        """
        Format query results into natural language response.
        
        Args:
            prompt: Results with formatting instructions.
            
        Returns:
            Formatted natural language response.
            
        Raises:
            RuntimeError: If formatter model not loaded.
        """
        if self.formatter_model is None:
            raise RuntimeError("Formatter model not loaded. Call load_response_formatter() first")
        
        response = self.formatter_model(
            prompt,
            max_new_tokens=FORMAT_MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=0.95,
            repetition_penalty=1.1,
            stop=["\n\n"]
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


