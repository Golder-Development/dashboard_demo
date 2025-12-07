"""
Test script to verify parliamentary sitting grouping works correctly
"""
import pandas as pd
import sys
from pathlib import Path

# Create test data
test_data = pd.DataFrame({
    'RegulatedEntityName': ['Entity A', 'Entity A', 'Entity A', 'Entity B', 'Entity B'],
    'parliamentary_sitting': [2010, 2010, 2015, 2010, 2015],
    'EventCount': [1, 1, 1, 1, 1]
})

print("Test Data:")
print(test_data)
print()

# Import calculations
from components.calculations import determine_groups_optimized
from config import THRESHOLDS

print("Thresholds:")
for k, v in THRESHOLDS.items():
    print(f"  {k}: {v}")
print()

# Test WITHOUT groupby_column (should group by lifetime totals)
print("=" * 80)
print("TEST 1: WITHOUT groupby_column (lifetime totals)")
print("=" * 80)
result_lifetime = determine_groups_optimized(
    test_data.copy(),
    'RegulatedEntityName',
    'EventCount',
    THRESHOLDS,
    groupby_column=None
)
print("\nEntity A has 3 total donations -> should be 'Small Entity'")
print("Entity B has 2 total donations -> should be 'Very Small Entity'")
print("\nActual results:")
print(result_lifetime)
print()

# Test WITH groupby_column (should group per parliament)
print("=" * 80)
print("TEST 2: WITH groupby_column='parliamentary_sitting' (per parliament)")
print("=" * 80)
result_parliament = determine_groups_optimized(
    test_data.copy(),
    'RegulatedEntityName',
    'EventCount',
    THRESHOLDS,
    groupby_column='parliamentary_sitting'
)
print("\nEntity A in 2010 parliament: 2 donations -> should be 'Very Small Entity'")
print("Entity A in 2015 parliament: 1 donation -> should be 'Single Donation Entity'")
print("Entity B in 2010 parliament: 1 donation -> should be 'Single Donation Entity'")
print("Entity B in 2015 parliament: 1 donation -> should be 'Single Donation Entity'")
print("\nActual results:")
print(result_parliament)
print()

# Verify results
print("=" * 80)
print("VERIFICATION")
print("=" * 80)
if result_lifetime[0] == 'Small Entity' and result_lifetime[3] == 'Very Small Entity':
    print("✓ Lifetime grouping works correctly")
else:
    print("✗ Lifetime grouping FAILED")
    print(f"  Entity A: {result_lifetime[0]} (expected: 'Small Entity')")
    print(f"  Entity B: {result_lifetime[3]} (expected: 'Very Small Entity')")

if (result_parliament[0] == 'Very Small Entity' and 
    result_parliament[2] == 'Single Donation Entity' and
    result_parliament[3] == 'Single Donation Entity' and
    result_parliament[4] == 'Single Donation Entity'):
    print("✓ Parliamentary sitting grouping works correctly")
else:
    print("✗ Parliamentary sitting grouping FAILED")
    print(f"  Entity A 2010: {result_parliament[0]} (expected: 'Very Small Entity')")
    print(f"  Entity A 2015: {result_parliament[2]} (expected: 'Single Donation Entity')")
    print(f"  Entity B 2010: {result_parliament[3]} (expected: 'Single Donation Entity')")
    print(f"  Entity B 2015: {result_parliament[4]} (expected: 'Single Donation Entity')")
