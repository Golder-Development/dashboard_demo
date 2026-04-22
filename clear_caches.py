#!/usr/bin/env python
"""Clear Streamlit cache and prepare for data reload"""
import os
import shutil
from pathlib import Path

print("=" * 60)
print("CLEARING CACHES")
print("=" * 60)

# Streamlit cache locations
cache_paths = [
    os.path.expandvars(r"%USERPROFILE%\.streamlit\cache"),
    os.path.expandvars(r"%APPDATA%\.streamlit"),
    os.path.expandvars(r"%LOCALAPPDATA%\Streamlit"),
]

for cache_path in cache_paths:
    if os.path.exists(cache_path):
        print(f"\nFound: {cache_path}")
        try:
            shutil.rmtree(cache_path)
            print(f"  ✓ Cleared successfully")
        except Exception as e:
            print(f"  ✗ Error clearing: {e}")
    else:
        print(f"\nNot found: {cache_path}")

# Also clear any .pytest_cache
pytest_cache = ".pytest_cache"
if os.path.exists(pytest_cache):
    print(f"\nFound: {pytest_cache}")
    try:
        shutil.rmtree(pytest_cache)
        print(f"  ✓ Cleared successfully")
    except Exception as e:
        print(f"  ✗ Error: {e}")

# Clear __pycache__ directories
print("\nClearing Python cache directories (__pycache__)...")
for root, dirs, files in os.walk("."):
    if "__pycache__" in dirs:
        cache_dir = os.path.join(root, "__pycache__")
        try:
            shutil.rmtree(cache_dir)
            print(f"  ✓ {cache_dir}")
        except Exception as e:
            print(f"  ✗ {cache_dir}: {e}")

print("\n" + "=" * 60)
print("CACHE CLEARING COMPLETE")
print("=" * 60)
print("\nNote: Streamlit's session cache will be cleared on next app reload.")
print("The dashboard will reprocess all data files when you restart it.")
