"""
Script to append new donations data and remove duplicates
Appends Donations_accepted_by_political_parties_20260116.csv to 
Donations_accepted_by_political_parties.csv and removes duplicates based on ECRef
Works with both CSV and ZIP formats (automatically uses ZIP if available)
"""

import pandas as pd
import os
import zipfile
from datetime import datetime

# Define file paths
SOURCE_DIR = "source"
MAIN_FILE = os.path.join(SOURCE_DIR, "Donations_accepted_by_political_parties.csv")
NEW_FILE = os.path.join(SOURCE_DIR, "Donations_accepted_by_political_parties_20260116.csv")
BACKUP_FILE = os.path.join(SOURCE_DIR, f"Donations_accepted_by_political_parties_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

def read_csv_or_zip(filepath):
    """Read CSV from either ZIP file or regular CSV"""
    zip_path = filepath.replace('.csv', '.zip')
    if os.path.exists(zip_path):
        print(f"Reading from ZIP: {zip_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            csv_filename = os.path.basename(filepath)
            with zip_ref.open(csv_filename) as f:
                return pd.read_csv(f)
    elif os.path.exists(filepath):
        print(f"Reading from CSV: {filepath}")
        return pd.read_csv(filepath)
    else:
        return None

def save_to_zip(df, csv_filepath):
    """Save DataFrame to ZIP file"""
    zip_filepath = csv_filepath.replace('.csv', '.zip')
    csv_filename = os.path.basename(csv_filepath)
    
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        csv_string = df.to_csv(index=False)
        zip_ref.writestr(csv_filename, csv_string)
    
    return zip_filepath


def append_and_dedupe():
    """
    Append new donations data and remove duplicates
    """
    # Check if files exist (either CSV or ZIP)
    main_exists = os.path.exists(MAIN_FILE) or os.path.exists(MAIN_FILE.replace('.csv', '.zip'))
    new_exists = os.path.exists(NEW_FILE) or os.path.exists(NEW_FILE.replace('.csv', '.zip'))
    
    if not main_exists:
        print(f"Error: Main file not found: {MAIN_FILE} or .zip version")
        return False

    if not new_exists:
        print(f"Error: New file not found: {NEW_FILE} or .zip version")
        return False

    print(f"Loading main file: {MAIN_FILE}")
    df_main = read_csv_or_zip(MAIN_FILE)
    if df_main is None:
        print(f"Error: Could not read main file")
        return False
    initial_count = len(df_main)
    print(f"Main file has {initial_count:,} records")

    print(f"\nLoading new file: {NEW_FILE}")
    df_new = read_csv_or_zip(NEW_FILE)
    if df_new is None:
        print(f"Error: Could not read new file")
        return False
    new_count = len(df_new)
    print(f"New file has {new_count:,} records")

    # Create backup of main file (as ZIP)
    print(f"\nCreating backup ZIP: {BACKUP_FILE.replace('.csv', '.zip')}")
    save_to_zip(df_main, BACKUP_FILE)

    # Append new data
    print("\nAppending new data...")
    df_combined = pd.concat([df_main, df_new], ignore_index=True)
    combined_count = len(df_combined)
    print(f"Combined data has {combined_count:,} records")

    # Remove duplicates based on ECRef (unique donation reference)
    print("\nRemoving duplicates based on ECRef...")
    df_deduplicated = df_combined.drop_duplicates(subset=['ECRef'], keep='first')
    final_count = len(df_deduplicated)
    duplicates_removed = combined_count - final_count
    print(f"Removed {duplicates_removed:,} duplicate records")
    print(f"Final dataset has {final_count:,} records")

    # Reset index
    df_deduplicated = df_deduplicated.reset_index(drop=True)
    df_deduplicated['index'] = df_deduplicated.index

    # Reorder columns to match original (index first)
    cols = df_deduplicated.columns.tolist()
    if 'index' in cols:
        cols.remove('index')
        cols = ['index'] + cols
        df_deduplicated = df_deduplicated[cols]

    # Save the deduplicated data back to main file as ZIP
    zip_file = MAIN_FILE.replace('.csv', '.zip')
    print(f"\nSaving deduplicated data to: {zip_file}")
    save_to_zip(df_deduplicated, MAIN_FILE)
    
    # Remove old CSV if it exists
    if os.path.exists(MAIN_FILE):
        os.remove(MAIN_FILE)
        print(f"Removed old CSV file: {MAIN_FILE}")

    print("\n" + "="*60)
    print("SUMMARY:")
    print(f"  Initial records:      {initial_count:,}")
    print(f"  New records added:    {new_count:,}")
    print(f"  Duplicates removed:   {duplicates_removed:,}")
    print(f"  Final record count:   {final_count:,}")
    print(f"  Net new records:      {final_count - initial_count:,}")
    print("="*60)
    print(f"\nBackup saved to: {BACKUP_FILE.replace('.csv', '.zip')}")
    print(f"Main file saved as: {zip_file}")
    print("Process completed successfully!")

    return True


if __name__ == "__main__":
    try:
        append_and_dedupe()
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()