import pandas as pd
from data.data_file_defs import load_cleaned_data
import config
import os

# Load the cleaned data
output_dir = config.DIRECTORIES["output_dir"]
cleaned_data_fname = config.FILENAMES["output_dir"]["cleaned_data_fname"]
cleaned_data_path = os.path.join(output_dir, cleaned_data_fname.replace('.zip', '.csv'))

print("Loading data...")
df = load_cleaned_data(cleaned_data_path)

print(f"Loaded {len(df)} rows")
print(f"Columns: {df.columns.tolist()[:10]}...")

# Test the groupby operation that plot_bar_line uses
print("\n\nTesting groupby operation like plot_bar_line_by_year...")
try:
    grouped = df.groupby(["YearReceived", "RegulatedEntityType"], observed=True)["EventCount"].sum().reset_index()
    print(f"Grouped shape: {grouped.shape}")
    print(f"Grouped head:\n{grouped.head(20)}")
    print(f"\nGrouped sum of EventCount: {grouped['EventCount'].sum()}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test the groupby operation that pie chart uses
print("\n\nTesting groupby operation like pie chart...")
try:
    grouped2 = df.groupby("Party_Group", observed=True, as_index=False)["Value"].sum()
    print(f"Grouped shape: {grouped2.shape}")
    print(f"Grouped head:\n{grouped2.head(20)}")
    print(f"\nGrouped sum of Value: {grouped2['Value'].sum()}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
