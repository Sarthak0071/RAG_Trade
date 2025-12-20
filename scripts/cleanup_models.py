import shutil
from pathlib import Path

cache_dir = Path.home() / ".cache" / "huggingface" / "hub"

print("Cleaning HuggingFace cache...")

if cache_dir.exists():
    total_size = 0
    deleted_count = 0
    
    for model_dir in cache_dir.iterdir():
        if "mistral" in model_dir.name.lower() or "llama" in model_dir.name.lower():
            size = sum(f.stat().st_size for f in model_dir.rglob('*') if f.is_file()) / 1024**3
            total_size += size
            
            print(f"\nFound: {model_dir.name}")
            print(f"  Size: {size:.2f} GB")
            print(f"  Deleting...")
            
            shutil.rmtree(model_dir)
            deleted_count += 1
            print(f"  Deleted!")
    
    if deleted_count > 0:
        print(f"\nCleaned up {deleted_count} model(s)")
        print(f"Total space freed: {total_size:.2f} GB")
    else:
        print("\nNo Mistral/Llama models found in cache")
else:
    print("No HuggingFace cache directory found")

print("\nCleanup complete!")
