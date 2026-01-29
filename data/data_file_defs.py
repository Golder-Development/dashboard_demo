import pandas as pd
import zipfile
import os
import config


def _read_csv_from_zip_or_csv(filepath):
    """Helper function to read CSV from ZIP file or regular CSV"""
    # Check if ZIP version exists
    zip_path = filepath.replace('.csv', '.zip')
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get the CSV filename from the original path
            csv_filename = os.path.basename(filepath)
            with zip_ref.open(csv_filename) as f:
                return f
    # Fallback to regular CSV if ZIP doesn't exist
    return filepath


def save_dataframe_to_zip(df, csv_filepath, index=True):
    """Helper function to save DataFrame to ZIP file"""
    # Check if csv_filepath is already a zip reference
    if csv_filepath.endswith('.zip'):
        zip_filepath = csv_filepath
        csv_filename = os.path.basename(csv_filepath).replace('.zip', '.csv')
    else:
        zip_filepath = csv_filepath.replace('.csv', '.zip')
        csv_filename = os.path.basename(csv_filepath)

    # If no directory was provided, default to output directory
    if not os.path.dirname(zip_filepath):
        output_dir = config.DIRECTORIES.get("output_dir", "")
        zip_filepath = os.path.join(output_dir, zip_filepath)
    
    # Create parent directory if it doesn't exist
    dir_path = os.path.dirname(zip_filepath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        csv_string = df.to_csv(index=index)
        zip_ref.writestr(csv_filename, csv_string)
    
    return zip_filepath


def load_source_data(originaldatafilepath):
    loaddata_df = pd.read_csv(
        _read_csv_from_zip_or_csv(originaldatafilepath),
        dtype={
            "ECRef": "object",
            "RegulatedEntityName": "object",
            "RegulatedEntityType": "object",
            "Value": "object",
            "AcceptedDate": "object",
            "AccountingUnitName": "object",
            "DonorName": "object",
            "AccountingUnitsAsCentralParty": "object",
            "IsSponsorship": "string",
            "DonorStatus": "object",
            "RegulatedDoneeType": "object",
            "CompanyRegistrationNumber": "object",
            "Postcode": "object",
            "DonationType": "object",
            "NatureOfDonation": "object",
            "PurposeOfVisit": "object",
            "DonationAction": "object",
            "ReceivedDate": "object",
            "ReportedDate": "object",
            "IsReportedPrePoll": "string",
            "ReportingPeriodName": "object",
            "IsBequest": "string",
            "IsAggregation": "string",
            "RegulatedEntityId": "object",
            "AccountingUnitId": "object",
            "DonorId": "object",
            "CampaigningName": "object",
            "RegisterName": "object",
            "IsIrishSource": "string",
        },
        index_col=0,
    )
    return loaddata_df


def load_improved_raw_data(originaldatafilepath):
    loaddata_df = pd.read_csv(
        _read_csv_from_zip_or_csv(originaldatafilepath),
        dtype={
            "ECRef": "object",
            "RegulatedEntityName": "object",
            "RegulatedEntityType": "object",
            "Value": "float64",
            "AcceptedDate": "object",
            "AccountingUnitName": "object",
            "DonorName": "object",
            "AccountingUnitsAsCentralParty": "object",
            "IsSponsorship": "string",
            "DonorStatus": "object",
            "RegulatedDoneeType": "object",
            "CompanyRegistrationNumber": "object",
            "Postcode": "object",
            "DonationType": "object",
            "NatureOfDonation": "object",
            "PurposeOfVisit": "object",
            "DonationAction": "object",
            "ReceivedDate": "object",
            "ReportedDate": "object",
            "IsReportedPrePoll": "string",
            "ReportingPeriodName": "object",
            "IsBequest": "string",
            "IsAggregation": "string",
            "RegulatedEntityId": "int64",
            "AccountingUnitId": "object",
            "DonorId": "oint64",
            "CampaigningName": "object",
            "RegisterName": "object",
            "IsIrishSource": "string",
        },
        index_col=0,
    )
    return loaddata_df


def load_cleaned_donations(originaldatafilepath):
    loaddata_df = pd.read_csv(
        _read_csv_from_zip_or_csv(originaldatafilepath),
        dtype={
            "ECRef": "object",
            "OriginalRegulatedEntityName": "object",
            "RegulatedEntityName": "object",
            "RegulatedEntityType": "object",
            "Value": "float64",
            "AcceptedDate": "object",
            "AccountingUnitName": "object",
            "OriginalDonorName": "object",
            "AccountingUnitsAsCentralParty": "object",
            "IsSponsorship": "string",
            "DonorStatus": "object",
            "RegulatedDoneeType": "object",
            "CompanyRegistrationNumber": "object",
            "Postcode": "object",
            "DonationType": "object",
            "NatureOfDonation": "object",
            "PurposeOfVisit": "object",
            "DonationAction": "object",
            "ReceivedDate": "object",
            "ReportedDate": "object",
            "IsReportedPrePoll": "string",
            "ReportingPeriodName": "object",
            "IsBequest": "string",
            "IsAggregation": "string",
            "OriginalRegulatedEntityId": "int64",
            "AccountingUnitId": "object",
            "OriginalDonorId": "int64",
            "CampaigningName": "object",
            "RegisterName": "object",
            "IsIrishSource": "string",
            "CleanedRegulatedEntityName": "object",
            "CleanedRegulatedEntityId": "int64",
            "RegulatedEntityId": "int64",
            "CleanedDonorName": "object",
            "CleanedDonorId": "int64",
            "DonorId": "int64",
            "DonorName": "object",
        },
        index_col=0,)

    return loaddata_df


def load_cleaned_data(originaldatafilepath):
    loaddata_df = pd.read_csv(
        _read_csv_from_zip_or_csv(originaldatafilepath),
        dtype={
            "ECRef": "object",
            "OriginalRegulatedEntityName": "object",
            "RegulatedEntityType": "object",
            "Value": "float64",
            "OriginalDonorName": "object",
            "IsSponsorship": "string",
            "DonorStatus": "object",
            "RegulatedDoneeType": "object",
            "DonationType": "object",
            "NatureOfDonation": "object",
            "PurposeOfVisit": "object",
            "DonationAction": "object",
            "ReportingPeriodName": "object",
            "IsBequest": "string",
            "IsAggregation": "string",
            "OriginalRegulatedEntityId": "int64",
            "OriginalDonorId": "int64",
            "CampaigningName": "object",
            "RegisterName": "object",
            "CleanedRegulatedEntityName": "object",
            "CleanedRegulatedEntityId": "int64",
            "RegulatedEntityId": "int64",
            "RegulatedEntityName": "object",
            "CleanedDonorName": "object",
            "CleanedDonorId": "int64",
            "DonorId": "int64",
            "DonorName": "object",
            "EventCount": "int64",
            "YearReceived": "int64",
            "MonthReceived": "int64",
            "YearMonthReceived": "int64",
            "PartyName": "object",
            "PartyId": "int64",
            "DubiousDonor": "int64",
            "DubiousData": "int64",
            "RegEntity_Group": "object",
            "DonationTypeInt": "int64",
            "RegulatedEntityNameInt": "int64",
            "DonorNameInt": "int64",
            "DonationActionInt": "int64",
            "DonorStatusInt": "int64",
            "PurposeOfVisitInt": "int64",
            "RegulatedDoneeTypeInt": "int64",
            "IsBequestInt": "int64",
            "IsAggregationInt": "int64",
            "IsSponsorshipInt": "int64",
            "NatureOfDonationInt": "int64",
            "RegisterNameInt": "int64",
            "PublicFundsInt": "int64",
            "DaysTillNextElection": "int64",
            "DaysSinceLastElection": "int64",
            "WksTillNextElection": "int64",
            "WksSinceLastElection": "int64",
            "QtrsTillNextElection": "int64",
            "QtrsSinceLastElection": "int64",
            "YrsTillNextElection": "int64",
            "YrsSinceLastElection": "int64",
            "parliamentary_sitting": "object",
        },
        parse_dates=["ReceivedDate"],
        index_col=0,)

    return loaddata_df


def load_donor_list(originaldatafilepath):
    loaddata_df = pd.read_csv(
        _read_csv_from_zip_or_csv(originaldatafilepath),
        dtype={
            "DonorId": "int64",
            "DonorName": "object",
            "DonorType": "object",
            "CompanyRegistrationNumber": "object",
            "Address": "object",
            "Postcode": "object",
            "Country": "object",
            "IsIrishSource": "string",
        },
        index_col="DonorId",
    )
    
    return loaddata_df
