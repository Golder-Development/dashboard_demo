# ZIP File Compression Implementation - Summary

## Overview
All large CSV data files are now stored as ZIP files to save approximately 90% disk space while maintaining full functionality. The system transparently handles both CSV and ZIP formats.

## Files Modified

### 1. Core Data Loading (`data/data_file_defs.py`)
**Changes:**
- Added `_read_csv_from_zip_or_csv()` helper function to read from ZIP or CSV
- Added `save_dataframe_to_zip()` helper function to save DataFrames as compressed ZIP
- Updated all load functions to use ZIP helper:
  - `load_source_data()`
  - `load_improved_raw_data()`
  - `load_cleaned_donations()`
  - `load_cleaned_data()`
  - `load_donor_list()`

**Behavior:**
- Automatically checks for `.zip` version first
- Falls back to `.csv` if ZIP doesn't exist
- Transparent to calling code

### 2. Data Saving Functions
**Files Updated:**
- `data/raw_data_clean.py` - Line 225: Save imported_raw.csv as ZIP
- `data/clean_and_enhance.py` - Line 580: Save cleaned_data.csv as ZIP
- `data/datasetupandclean.py` - Line 107: Save raw data as ZIP
- `data/load_donor_regent_lists.py` - Lines 67, 137, 208: Save donor/entity lists as ZIP

**Changes:**
- Replaced `df.to_csv()` calls with `save_dataframe_to_zip()` function
- Updated log messages to reflect ZIP file paths

### 3. Append and Dedupe Script (`append_and_dedupe_donations.py`)
**New Features:**
- `read_csv_or_zip()` function - reads from either format
- `save_to_zip()` function - saves output as ZIP
- Checks for both CSV and ZIP versions of input files
- Saves backups as ZIP files
- Removes old CSV after creating ZIP
- Updated all file operations to use ZIP format

**Behavior:**
- Automatically detects and reads from ZIP or CSV
- Creates compressed backups
- Outputs compressed main file
- Reports space savings

### 4. New Utility Script (`convert_csv_to_zip.py`)
**Purpose:** One-time conversion of existing CSV files to ZIP format

**Features:**
- Converts specified large CSV files to ZIP
- Shows compression statistics (original size, compressed size, savings %)
- Removes original CSV files after compression
- Provides summary report

**Target Files:**
- `source/Donations_accepted_by_political_parties.csv`
- `output/cleaned_data.csv`
- `output/cleaned_donations.csv`
- `output/imported_raw.csv`

### 5. Documentation (`README.md`)
**Additions:**
- New "Converting Existing CSV Files to ZIP" section
- Updated "Updating Data" section to mention ZIP support
- Added notes about automatic ZIP compression
- Updated file paths to mention `.zip` versions
- Added space savings information (~90% compression)

## How It Works

### Reading Data
1. Check if `.zip` version exists
2. If yes, open ZIP and read CSV from inside
3. If no, fall back to regular `.csv` file
4. Return DataFrame to caller (transparent operation)

### Writing Data
1. Convert DataFrame to CSV string
2. Create ZIP file with same base name
3. Write CSV string into ZIP with compression
4. Log ZIP file path

### File Naming Convention
- Original: `filename.csv`
- Compressed: `filename.zip` (contains `filename.csv` inside)

## Benefits

1. **Space Savings:** ~90% reduction in disk usage
2. **Backward Compatible:** Still works with CSV files if ZIP not available
3. **Transparent:** No changes needed to dashboard code logic
4. **Automatic:** System automatically prefers ZIP over CSV
5. **Git Friendly:** Smaller files are easier to manage in version control

## Usage Instructions

### For New Installations
Just run normally - files will be created as ZIP automatically

### For Existing Installations
1. Run conversion utility once:
   ```bash
   python convert_csv_to_zip.py
   ```
2. Continue using dashboard normally

### Updating Data
- New data files can be CSV or ZIP
- `append_and_dedupe_donations.py` handles both formats automatically
- Output is always saved as ZIP

## Technical Details

### Compression Method
- Uses `zipfile.ZIP_DEFLATED` (standard ZIP compression)
- Compression level: Default (good balance of speed/size)
- Format: Standard ZIP archive

### Error Handling
- Falls back to CSV if ZIP read fails
- Creates parent directories if they don't exist
- Provides clear error messages

### Performance
- Slight CPU overhead for compression/decompression
- Minimal impact on load times (I/O time saved from smaller files)
- Overall net performance improvement for large files

## Testing Checklist

- [ ] Dashboard loads data from ZIP files correctly
- [ ] Data refresh mechanism detects ZIP file changes
- [ ] Append script works with existing ZIP files
- [ ] Conversion utility compresses files successfully
- [ ] Backup creation works with ZIP format
- [ ] All data pipelines function correctly
- [ ] No errors in logs related to file operations

## Rollback Plan

If issues occur:
1. Decompress ZIP files to CSV:
   ```python
   import zipfile
   import os
   
   for zip_file in ["file1.zip", "file2.zip"]:
       with zipfile.ZipFile(zip_file, 'r') as z:
           z.extractall(os.path.dirname(zip_file))
       os.remove(zip_file)
   ```
2. Revert code changes
3. Dashboard will work with CSV files

## Future Enhancements

Potential improvements:
- Configurable compression level
- Support for other compression formats (gzip, bz2)
- Parallel compression for multiple files
- Progress bars for large file operations
- Automatic cleanup of old backup files
