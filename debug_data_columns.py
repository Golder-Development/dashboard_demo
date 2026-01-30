"""
Debug script to check what columns are available in the loaded data
and if EventCount is present.
"""
import pandas as pd
from data.data_file_defs import load_cleaned_data
import config
import os

# Load the cleaned data
print("Loading cleaned data...")
output_dir = config.DIRECTORIES["output_dir"]
cleaned_data_fname = config.FILENAMES["output_dir"]["cleaned_data_fname"]
# Build the full path but pass the .csv version to the loader
cleaned_data_path = os.path.join(output_dir, cleaned_data_fname.replace('.zip', '.csv'))
print(f"Path: {cleaned_data_path}")

df = load_cleaned_data(cleaned_data_path)

print(f"\nDataFrame shape: {df.shape}")
print(f"\nColumns in DataFrame:")
print(df.columns.tolist())

print(f"\nFirst few rows:")
print(df.head())

# Check if EventCount exists
if "EventCount" in df.columns:
    print(f"\n✓ EventCount column EXISTS")
    print(f"EventCount values: {df['EventCount'].unique()[:10]}")
    print(f"EventCount dtype: {df['EventCount'].dtype}")
    print(f"EventCount sum: {df['EventCount'].sum()}")
else:
    print(f"\n✗ EventCount column MISSING!")

# Check Value column
if "Value" in df.columns:
    print(f"\n✓ Value column EXISTS")
    print(f"Value dtype: {df['Value'].dtype}")
    print(f"Value sum: {df['Value'].sum()}")
else:
    print(f"\n✗ Value column MISSING!")

# Check YearReceived
if "YearReceived" in df.columns:
    print(f"\n✓ YearReceived column EXISTS")
    print(f"YearReceived unique values: {sorted(df['YearReceived'].unique())}")
else:
    print(f"\n✗ YearReceived column MISSING!")

# Test groupby aggregation
print("\n\nTesting groupby aggregation...")
try:
    grouped = df.groupby(["YearReceived", "RegulatedEntityType"], observed=True)["EventCount"].sum().reset_index()
    print(f"Grouped data shape: {grouped.shape}")
    print(f"Grouped data:\n{grouped.head(10)}")
except Exception as e:
    print(f"Error during groupby: {e}")

print("\n\nChecking for any columns with all zeros or nulls...")
for col in df.columns:
    if df[col].dtype in ['int64', 'float64']:
        if df[col].sum() == 0:
            print(f"WARNING: Column '{col}' has all zeros!")
        if df[col].isna().all():
            print(f"WARNING: Column '{col}' is all nulls!")
