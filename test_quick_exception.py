"""
Quick test to verify party exception handling works
"""
import pandas as pd
from components.calculations import determine_groups_optimized
from config import THRESHOLDS, DATA_REMAPPINGS

# Test data
test_data = pd.DataFrame({
    'RegulatedEntityName': [
        'Conservative And Unionist Party',
        'Labour Party',
        'Liberal Democrats',
        'Scottish National Party (Snp)',
        'Regular Donor Ltd'
    ],
    'parliamentary_sitting': [2010, 2010, 2010, 2010, 2010],
    'EventCount': [1, 1, 1, 1, 1]
})

party_parents = DATA_REMAPPINGS["PartyParents"]

result = determine_groups_optimized(
    test_data.copy(),
    'RegulatedEntityName',
    'EventCount',
    THRESHOLDS,
    exception_dict=party_parents,
    groupby_column='parliamentary_sitting'
)

print("Entity Name -> Group Assignment")
print("-" * 60)
for idx, row in test_data.iterrows():
    print(f"{row['RegulatedEntityName']:40s} -> {result[idx]}")

print("\n" + "="*60)
print("SUMMARY:")
print("="*60)

# Check if major parties are excepted
major_parties = ['Conservative And Unionist Party', 'Labour Party', 
                 'Liberal Democrats', 'Scottish National Party (Snp)']
excepted_count = sum(1 for idx, name in enumerate(test_data['RegulatedEntityName']) 
                     if name in major_parties and result[idx] == name)
regular_count = sum(1 for idx, name in enumerate(test_data['RegulatedEntityName']) 
                    if name not in major_parties and 'Entity' in result[idx])

print(f"Major parties excepted: {excepted_count}/4")
print(f"Regular donors categorized: {regular_count}/1")

if excepted_count == 4 and regular_count == 1:
    print("\nSUCCESS: All exception handling working correctly!")
else:
    print("\nFAILURE: Exception handling not working as expected")
