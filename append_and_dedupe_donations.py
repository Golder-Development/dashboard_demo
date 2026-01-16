"""
Script to append new donations data and remove duplicates
Appends Donations_accepted_by_political_parties_20260116.csv to 
Donations_accepted_by_political_parties.csv and removes duplicates based on ECRef
"""

import pandas as pd
import os
from datetime import datetime

# Define file paths
SOURCE_DIR = "source"
MAIN_FILE = os.path.join(SOURCE_DIR, "Donations_accepted_by_political_parties.csv")
NEW_FILE = os.path.join(SOURCE_DIR, "Donations_accepted_by_political_parties_20260116.csv")
BACKUP_FILE = os.path.join(SOURCE_DIR, f"Donations_accepted_by_political_parties_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")


def append_and_dedupe():
    """
    Append new donations data and remove duplicates
    """
    # Check if files exist
    if not os.path.exists(MAIN_FILE):
        print(f"Error: Main file not found: {MAIN_FILE}")
        return False

    if not os.path.exists(NEW_FILE):
        print(f"Error: New file not found: {NEW_FILE}")
        return False

    print(f"Loading main file: {MAIN_FILE}")
    df_main = pd.read_csv(MAIN_FILE)
    initial_count = len(df_main)
    print(f"Main file has {initial_count:,} records")

    print(f"\nLoading new file: {NEW_FILE}")
    df_new = pd.read_csv(NEW_FILE)
    new_count = len(df_new)
    print(f"New file has {new_count:,} records")

    # Create backup of main file
    print(f"\nCreating backup: {BACKUP_FILE}")
    df_main.to_csv(BACKUP_FILE, index=False)

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

    # Save the deduplicated data back to main file
    print(f"\nSaving deduplicated data to: {MAIN_FILE}")
    df_deduplicated.to_csv(MAIN_FILE, index=False)

    print("\n" + "="*60)
    print("SUMMARY:")
    print(f"  Initial records:      {initial_count:,}")
    print(f"  New records added:    {new_count:,}")
    print(f"  Duplicates removed:   {duplicates_removed:,}")
    print(f"  Final record count:   {final_count:,}")
    print(f"  Net new records:      {final_count - initial_count:,}")
    print("="*60)
    print(f"\nBackup saved to: {BACKUP_FILE}")
    print("Process completed successfully!")

    return True


if __name__ == "__main__":
    try:
        append_and_dedupe()
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()