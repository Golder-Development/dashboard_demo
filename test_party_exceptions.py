"""
Test that party exception handling works with parliamentary sitting grouping
"""
import pandas as pd

# Create test data with realistic party names
test_data = pd.DataFrame({
    'RegulatedEntityName': [
        'Conservative And Unionist Party',  # Should be excepted
        'Conservative And Unionist Party',  # Should be excepted
        'Labour Party',  # Should be excepted
        'Liberal Democrats',  # Should be excepted
        'Regular Donor Ltd',  # Regular threshold grouping
        'Regular Donor Ltd'  # Regular threshold grouping
    ],
    'parliamentary_sitting': [2010, 2015, 2010, 2015, 2010, 2015],
    'EventCount': [1, 1, 1, 1, 1, 1]
})

print("Test Data:")
print(test_data)
print()

# Import calculations
from components.calculations import determine_groups_optimized
from config import THRESHOLDS, DATA_REMAPPINGS

party_parents = DATA_REMAPPINGS["PartyParents"]

print("PartyParents exception dict:")
for k, v in party_parents.items():
    print(f"  {k}: {v}")
print()

# Test WITH exceptions and groupby_column
print("=" * 80)
print("TEST: With parliamentary_sitting grouping AND party exceptions")
print("=" * 80)
result = determine_groups_optimized(
    test_data.copy(),
    'RegulatedEntityName',
    'EventCount',
    THRESHOLDS,
    exception_dict=party_parents,
    groupby_column='parliamentary_sitting'
)

print("\nExpected Results:")
print("  Conservative And Unionist Party (all) -> 'Conservative And Unionist Party' (excepted)")
print("  Labour Party (all) -> 'Labour Party' (excepted)")
print("  Liberal Democrats (all) -> 'Liberal Democrats' (excepted)")
print("  Regular Donor Ltd (all) -> 'Single Donation Entity' (1 donation per parliament)")
print()
print("Actual Results:")
print(result)
print()

# Verification
print("=" * 80)
print("VERIFICATION")
print("=" * 80)

# Check that major parties are excepted (returned as their own names)
conservative_results = result[test_data['RegulatedEntityName'] == 'Conservative And Unionist Party']
labour_results = result[test_data['RegulatedEntityName'] == 'Labour Party']
libdem_results = result[test_data['RegulatedEntityName'] == 'Liberal Democrats']
regular_results = result[test_data['RegulatedEntityName'] == 'Regular Donor Ltd']

if all(conservative_results == 'Conservative And Unionist Party'):
    print("✓ Conservative Party correctly excepted (not categorized by threshold)")
else:
    print("✗ Conservative Party exception FAILED")
    print(f"  Got: {conservative_results.unique()}")

if all(labour_results == 'Labour Party'):
    print("✓ Labour Party correctly excepted")
else:
    print("✗ Labour Party exception FAILED")
    print(f"  Got: {labour_results.unique()}")

if all(libdem_results == 'Liberal Democrats'):
    print("✓ Liberal Democrats correctly excepted")
else:
    print("✗ Liberal Democrats exception FAILED")
    print(f"  Got: {libdem_results.unique()}")

if all(regular_results == 'Single Donation Entity'):
    print("✓ Regular donor correctly categorized by threshold")
else:
    print("✗ Regular donor categorization FAILED")
    print(f"  Got: {regular_results.unique()}")
    print(f"  Expected: 'Single Donation Entity'")
