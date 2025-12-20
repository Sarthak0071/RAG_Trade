from huggingface_hub import hf_hub_download
import os
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='huggingface_hub')

MODELS = {
    "mistral_sql": {
        "repo": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        "filename": "mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        "size": "4.1 GB",
        "purpose": "SQL Generation"
    },
    "tinyllama_formatter": {
        "repo": "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        "filename": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "size": "0.6 GB",
        "purpose": "Response Formatting"
    }
}

def download_model(model_name):
    config = MODELS[model_name]
    print(f"\nModel: {model_name}")
    print(f"Purpose: {config['purpose']}")
    print(f"File: {config['filename']}")
    print(f"Size: ~{config['size']}")
    
    model_dir = os.path.join("models", model_name)
    os.makedirs(model_dir, exist_ok=True)
    
    print("\nDownloading (this may take several minutes)...")
    print("Progress bar will appear below:")
    
    filepath = hf_hub_download(
        repo_id=config['repo'],
        filename=config['filename'],
        local_dir=model_dir
    )
    
    print(f"\nCompleted: {filepath}\n")
    return filepath

if __name__ == "__main__":
    print("RAG System - GGUF Model Downloader")
    print("\nUsing GGUF format (pre-quantized, smaller, faster)")
    print("\nModels to download:")
    print("  1. Mistral-7B-Instruct (SQL Generation) - 4.1 GB")
    print("  2. TinyLlama-1.1B (Response Formatting) - 0.6 GB")
    print("\nTotal download size: ~4.7 GB")
    print("\nNote: Warnings about 'Xet Storage' are harmless and can be ignored.")
    
    choice = input("\nProceed with download? (y/n): ")
    if choice.lower() != 'y':
        print("Download cancelled")
        exit()
    
    print("\nStarting downloads...")
    sql_model_path = download_model("mistral_sql")
    format_model_path = download_model("tinyllama_formatter")
    
    print("\nDownload Complete")
    print(f"\nSQL Generator: {sql_model_path}")
    print(f"Formatter: {format_model_path}")
    print("\nBoth models saved to 'models/' folder")
    print("Ready for Phase 2")


