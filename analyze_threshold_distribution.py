"""
Analyze donation distribution per entity per parliamentary sitting
to design meaningful thresholds for per-parliament analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Load the cleaned data
output_dir = Path("output")
cleaned_data_path = output_dir / "cleaned_data.csv"

if not cleaned_data_path.exists():
    print(f"Error: {cleaned_data_path} not found")
    sys.exit(1)

print("Loading cleaned data...")
df = pd.read_csv(cleaned_data_path)

# Check if parliamentary_sitting column exists
if 'parliamentary_sitting' not in df.columns:
    print("Error: 'parliamentary_sitting' column not found in cleaned data")
    print(f"Available columns: {df.columns.tolist()}")
    sys.exit(1)

print(f"Total rows: {len(df)}")
print(f"Date range: {df['ReceivedDate'].min()} to {df['ReceivedDate'].max()}")
print(f"\nParliamentary sittings found:")
print(df['parliamentary_sitting'].unique())

# Group by RegulatedEntityName and parliamentary_sitting to get donation counts
print("\n" + "="*80)
print("ANALYZING DONATION DISTRIBUTION PER ENTITY PER PARLIAMENT")
print("="*80)

entity_parliament_counts = df.groupby(
    ['RegulatedEntityName', 'parliamentary_sitting']
).size().reset_index(name='donation_count')

print(f"\nTotal entity-parliament combinations: {len(entity_parliament_counts)}")

# Exclude single donation entities for threshold distribution
multi_donation_entities = entity_parliament_counts[
    entity_parliament_counts['donation_count'] > 1
].copy()

print(f"Entity-parliament combos with >1 donation: {len(multi_donation_entities)}")
print(f"Entity-parliament combos with exactly 1 donation: {len(entity_parliament_counts) - len(multi_donation_entities)}")

# Statistics for multi-donation entities
print("\n" + "-"*80)
print("DISTRIBUTION STATISTICS (excluding single-donation entities)")
print("-"*80)

stats = {
    'Mean': multi_donation_entities['donation_count'].mean(),
    'Median': multi_donation_entities['donation_count'].median(),
    'Min': multi_donation_entities['donation_count'].min(),
    'Max': multi_donation_entities['donation_count'].max(),
    'Std Dev': multi_donation_entities['donation_count'].std(),
    '25th percentile': multi_donation_entities['donation_count'].quantile(0.25),
    '50th percentile': multi_donation_entities['donation_count'].quantile(0.50),
    '75th percentile': multi_donation_entities['donation_count'].quantile(0.75),
    '90th percentile': multi_donation_entities['donation_count'].quantile(0.90),
    '95th percentile': multi_donation_entities['donation_count'].quantile(0.95),
}

for key, value in stats.items():
    print(f"{key:20s}: {value:8.2f}")

# Quartile-based distribution (6 even-spread categories)
print("\n" + "-"*80)
print("QUARTILE/PERCENTILE ANALYSIS FOR 6 EVEN-SPREAD CATEGORIES")
print("-"*80)

# Divide into 6 even spreads using percentiles
percentiles = [0, 1/6, 2/6, 3/6, 4/6, 5/6, 1.0]
percentile_values = [
    multi_donation_entities['donation_count'].quantile(p) 
    for p in percentiles
]

print("\nPercentile boundaries for 6 even-spread categories:")
for i, (pct, val) in enumerate(zip(percentiles, percentile_values)):
    print(f"  {pct*100:5.1f}th percentile: {val:7.1f}")

# Create threshold ranges based on percentiles
print("\n" + "-"*80)
print("PROPOSED THRESHOLDS (6 even-spread categories)")
print("-"*80)

proposed_thresholds = []
for i in range(len(percentile_values) - 1):
    lower = int(np.ceil(percentile_values[i]))
    upper = int(np.floor(percentile_values[i + 1]))
    
    # Ensure ranges don't overlap
    if i > 0:
        lower = max(lower, proposed_thresholds[-1][1] + 1)
    
    proposed_thresholds.append((lower, upper))
    
    # Count entities in this range
    count_in_range = len(multi_donation_entities[
        (multi_donation_entities['donation_count'] >= lower) &
        (multi_donation_entities['donation_count'] <= upper)
    ])
    
    print(f"  Range {i+1}: ({lower:3d}, {upper:3d}) - {count_in_range:4d} entity-parliament combos")

# Distribution check
print("\n" + "-"*80)
print("ACTUAL DISTRIBUTION IN PROPOSED RANGES")
print("-"*80)

range_labels = [
    "Very Small Entity",
    "Small Entity", 
    "Small Medium Entity",
    "Medium Entity",
    "Medium Large Entity",
    "Large Entity"
]

print(f"\n(0, 0):       'No Relevant Donations'")
print(f"(1, 1):       'Single Donation Entity'")

for (lower, upper), label in zip(proposed_thresholds, range_labels):
    count = len(multi_donation_entities[
        (multi_donation_entities['donation_count'] >= lower) &
        (multi_donation_entities['donation_count'] <= upper)
    ])
    pct = 100 * count / len(multi_donation_entities)
    print(f"({lower:3d}, {upper:3d}): '{label:25s}' - {count:4d} combos ({pct:5.1f}%)")

# Show some example entities and their per-parliament distribution
print("\n" + "-"*80)
print("EXAMPLE: Top 10 entities by total donations (showing per-parliament distribution)")
print("-"*80)

total_by_entity = df.groupby('RegulatedEntityName').size().sort_values(ascending=False)
print(f"\nTop 10 entities and their per-parliament donation counts:")

for entity in total_by_entity.head(10).index:
    parliament_counts = entity_parliament_counts[
        entity_parliament_counts['RegulatedEntityName'] == entity
    ].sort_values('donation_count', ascending=False)
    total = parliament_counts['donation_count'].sum()
    print(f"\n  {entity} (total: {total} donations)")
    for _, row in parliament_counts.iterrows():
        print(f"    {str(row['parliamentary_sitting']):10s}: {row['donation_count']:3d} donations")
