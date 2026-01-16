"""
Utility script to convert existing CSV files to ZIP format
Run this once to compress large CSV files and save disk space
"""

import os
import zipfile
import pandas as pd

# Define files to compress
FILES_TO_COMPRESS = [
    "source/Donations_accepted_by_political_parties.csv",
    "output/cleaned_data.csv",
    "output/cleaned_donations.csv",
    "output/imported_raw.csv",
]

def compress_csv_to_zip(csv_filepath):
    """Compress a CSV file to ZIP format"""
    if not os.path.exists(csv_filepath):
        print(f"⚠️  File not found: {csv_filepath}")
        return False
    
    zip_filepath = csv_filepath.replace('.csv', '.zip')
    csv_filename = os.path.basename(csv_filepath)
    
    # Get original file size
    original_size = os.path.getsize(csv_filepath)
    
    # Read and compress
    print(f"📦 Compressing: {csv_filepath}")
    df = pd.read_csv(csv_filepath)
    
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        csv_string = df.to_csv(index=False)
        zip_ref.writestr(csv_filename, csv_string)
    
    # Get compressed size
    compressed_size = os.path.getsize(zip_filepath)
    savings = (1 - compressed_size / original_size) * 100
    
    print(f"✓ Created: {zip_filepath}")
    print(f"  Original: {original_size / 1024 / 1024:.2f} MB")
    print(f"  Compressed: {compressed_size / 1024 / 1024:.2f} MB")
    print(f"  Space saved: {savings:.1f}%")
    
    # Remove original CSV
    os.remove(csv_filepath)
    print(f"✓ Removed original CSV file\n")
    
    return True

def main():
    """Convert all large CSV files to ZIP"""
    print("="*60)
    print("CSV to ZIP Conversion Utility")
    print("="*60 + "\n")
    
    total_original = 0
    total_compressed = 0
    files_processed = 0
    
    for filepath in FILES_TO_COMPRESS:
        if os.path.exists(filepath):
            original_size = os.path.getsize(filepath)
            if compress_csv_to_zip(filepath):
                files_processed += 1
                total_original += original_size
                zip_path = filepath.replace('.csv', '.zip')
                total_compressed += os.path.getsize(zip_path)
        else:
            print(f"⚠️  Skipping (not found): {filepath}\n")
    
    if files_processed > 0:
        total_savings = (1 - total_compressed / total_original) * 100
        print("="*60)
        print("SUMMARY:")
        print(f"  Files processed: {files_processed}")
        print(f"  Total original size: {total_original / 1024 / 1024:.2f} MB")
        print(f"  Total compressed size: {total_compressed / 1024 / 1024:.2f} MB")
        print(f"  Total space saved: {total_savings:.1f}% ({(total_original - total_compressed) / 1024 / 1024:.2f} MB)")
        print("="*60)
        print("\n✓ Conversion complete! Your dashboard will now use ZIP files automatically.")
    else:
        print("No files were processed. Either files don't exist or are already compressed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
