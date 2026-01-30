# Paul Golder - StreamList Political Donations Dashboard

## Created During Course with Code institute

* Currently built to work on Python 3.10.11 - may work on more recent releases.
* This repo was built based on learning with aid from ChatGpt and codepilot for issue fixing
    and also development guidance.
* A hosted version of the dashboard should be available at
    -   https://golder-development-dashboard-demo-politicalpartyanalysis-rctb68.streamlit.app/

* When first run the dashboard undertakes a data refresh which involves a level of deduplication
    this can take several minutes, the "Please wait while the data sets are being calculated"
    message will disappear when processing has completed.
* Please review the "Notes on Data and Manipulations" page of the app for assumptions and
    data manipulations undertaken as part of the analysis.
* Please credit "https://www.linkedin.com/in/paulgolder/" if you use this repo or the calculations
    in it in your own developments.

## How to use this repo

1. Fork this repo and copy the https URL of your forked streamlit-lesson repo
2. On your Dashboard, click on the New Workspace button
3. Paste in the URL you copied from GitHub earlier
4. Click Create
5. Wait for the workspace to open. This can take a few minutes.
6. Open a new terminal and `pip3 install -r requirements.txt`
7. Once requirements are all installed - use type 'streamlit run PoliticalPartyAnalysisDashboard.py'

## Updating Data

The dashboard automatically detects when source data has been updated and reprocesses accordingly. **Large data files are automatically stored as ZIP files to save space.**

### Method 1: Replace the Source File (Simple)

Simply replace `source/Donations_accepted_by_political_parties.csv` (or the `.zip` version) with your new data file. The dashboard will automatically detect the change on next launch and reload all data.

### Method 2: Append New Data (Recommended for Updates)

When you receive a new data export from the Electoral Commission:

1. Save the new file to the `source/` directory with a date suffix (e.g., `Donations_accepted_by_political_parties_20260116.csv`)
2. Run the append and dedupe script:

   ```bash
   python append_and_dedupe_donations.py
   ```

3. The script will:

   - Automatically read from ZIP or CSV files
   - Create an automatic timestamped backup (as ZIP)
   - Append the new data to the main file
   - Remove duplicates based on ECRef (unique donation reference)
   - Save the result as a compressed ZIP file
   - Provide a summary of records added/removed
4. Restart the dashboard to load the updated data

**Note:** 
- The script automatically creates ZIP backups: `source/Donations_accepted_by_political_parties_backup_[timestamp].zip`
- Large files are stored as ZIP to save ~90% disk space
- The system automatically reads from ZIP files when available, falling back to CSV if needed

### Data Refresh Mechanism

The dashboard uses an intelligent caching system that:
- Tracks file modification timestamps in `reference_files/last_modified_dates.json`
- Automatically reprocesses data when source files change
- Stores processed data in `output/` directory as ZIP files for faster subsequent loads
- Respects the full data pipeline: raw → cleaned → donations → donor/entity lists
- Transparently handles both CSV and ZIP file formats
