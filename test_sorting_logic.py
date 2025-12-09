import pandas as pd

# Simulate the grouping logic
data = {
    'PartyName': ['Labour', 'Labour', 'Labour', 'Conservative', 'Conservative', 'Liberal'],
    'Party_Group': ['Large', 'Medium', 'Small', 'Large', 'Single Donation', 'Medium'],
    'Value': [5000, 3000, 1000, 8000, 500, 2000]
}

grouped_data = pd.DataFrame(data)

# Sort PartyName by total value (descending)
party_totals = grouped_data.groupby('PartyName')['Value'].sum().sort_values(ascending=False)
party_order = party_totals.index.tolist()
print("Party order by total value (descending):", party_order)

# Pivot for stacked bar chart
pivot_data = grouped_data.pivot_table(
    index='PartyName',
    columns='Party_Group',
    values='Value',
    aggfunc='sum',
    fill_value=0
)

# Reorder pivot_data
pivot_data = pivot_data.reindex(party_order)

# Reorder columns by total donations (largest to smallest)
column_totals = pivot_data.sum().sort_values(ascending=False)
pivot_data = pivot_data[column_totals.index.tolist()]

print("\nFinal pivot data (X-axis: Parties desc by value, stacks: categories from large to small):")
print(pivot_data)
print("\nColumn order (donation categories, largest to smallest):", column_totals.index.tolist())
