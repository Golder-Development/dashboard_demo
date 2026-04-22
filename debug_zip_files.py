#!/usr/bin/env python
"""Debug script to check ZIP file integrity and data"""
import zipfile
import os
import pandas as pd

print("=" * 60)
print("CHECKING SOURCE DATA FILE")
print("=" * 60)

# Check source ZIP integrity
source_zip = 'source/Donations_accepted_by_political_parties.zip'
print(f'\nChecking {source_zip}...')
print(f'File exists: {os.path.exists(source_zip)}')
if os.path.exists(source_zip):
    print(f'File size: {os.path.getsize(source_zip):,} bytes')

try:
    with zipfile.ZipFile(source_zip, 'r') as z:
        print(f'ZIP contents: {z.namelist()}')
        for name in z.namelist():
            info = z.getinfo(name)
            print(f'  - {name}: {info.file_size:,} bytes')
except Exception as e:
    print(f'ERROR reading ZIP: {e}')

# Try to read the CSV from ZIP
print('\nAttempting to read CSV from ZIP...')
try:
    with zipfile.ZipFile(source_zip, 'r') as z:
        csv_name = [n for n in z.namelist() if n.endswith('.csv')][0]
        df = pd.read_csv(z.open(csv_name), nrows=5)
        print(f'Successfully read CSV from ZIP: {csv_name}')
        print(f'Shape: {df.shape}')
        print(f'Columns: {list(df.columns)[:5]}...')
except Exception as e:
    print(f'ERROR reading CSV from ZIP: {e}')

print("\n" + "=" * 60)
print("CHECKING OUTPUT DATA FILES")
print("=" * 60)

output_files = [
    'output/cleaned_donations.zip',
    'output/cleaned_data.zip',
    'output/cleaned_donorlist.zip',
    'output/cleaned_regentity.zip',
    'output/imported_raw.zip'
]

for filepath in output_files:
    print(f'\n{filepath}:')
    print(f'  Exists: {os.path.exists(filepath)}')
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        print(f'  Size: {file_size:,} bytes')
        if file_size > 0:
            try:
                with zipfile.ZipFile(filepath, 'r') as z:
                    contents = z.namelist()
                    print(f'  Contents: {contents}')
                    for name in contents:
                        info = z.getinfo(name)
                        print(f'    - {name}: {info.file_size:,} bytes')
            except Exception as e:
                print(f'  ERROR: {e}')
        else:
            print('  WARNING: File is empty!')

print("\n" + "=" * 60)
print("CHECKING REFERENCE FILES")
print("=" * 60)

# Check last_modified_dates.json
ref_file = 'reference_files/last_modified_dates.json'
print(f'\n{ref_file}:')
print(f'  Exists: {os.path.exists(ref_file)}')
if os.path.exists(ref_file):
    try:
        import json
        with open(ref_file, 'r') as f:
            data = json.load(f)
            print(f'  Content: {data}')
    except Exception as e:
        print(f'  ERROR: {e}')
