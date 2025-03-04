import pandas as pd
import streamlit as st
import os
from rapidfuzz import process, fuzz
from collections import defaultdict
from utils.logger import logger, log_function_call
# Import the is_file_updated function
from data.data_utils import is_file_updated


@log_function_call
def dedupe_entity_file(
    loaddata_dd_df,
    entity,
    map_filename,
    threshold=85,
    output_csv=False
    ):
    """
    Loads a dedupe mapping file from the reference folder and
    merges it with the original data. Merges on the field named
    {entity}id. If the file does not exist, the dedupe_entity_fuzzy
    function is called to dedupe the data and return the new data.
    """
    # Load the data prep - set field names
    originalentityname = f"Original{entity}Name"
    originalentityid = f"Original{entity}Id"
    entityname = f"{entity}Name"
    entityid = f"{entity}Id"
    cleanedentityname = f"Cleaned{entity}Name"
    cleanedentityid = f"Cleaned{entity}Id"

    # Check that the entity ID exists in the data
    if entityid not in loaddata_dd_df.columns:
        logger.error(f"{entityid} not found in data")
        raise ValueError(f"{entityid} not found in data")

    # Check if the mapping file exists in the session state
    map_file_path = st.session_state.get(map_filename)
    if not map_file_path:
        logger.error(f"{map_filename} not found in session state filenames")
        raise ValueError(f"{map_filename} not found in session state filenames")

    # File exists and contains data use it to dedupe the data
    # check {map_filename} exists and has data
    elif os.path.exists(map_file_path) and os.path.getsize(map_file_path) > 0:
        logger.info(f"Map file {map_filename} exists."
                    " Proceeding with deduplication.")
        # Load the dedupe map file
        re_dedupe_df = pd.read_csv(map_file_path)
        # Ensure that there is only one value for each entity ID by taking
        # the first value in all cases
        re_dedupe_df = re_dedupe_df.groupby(entityid).first().reset_index()
        # Merge the cleaned data with the original data, selecting only required columns
        loaddata_dd_df = pd.merge(loaddata_dd_df,
                      re_dedupe_df[[entityid, cleanedentityname, cleanedentityid]],
                      how="left",
                      on=entityid)
        # # Rename columns
        # entityname_x = f"{entityname}_x"
        # # entityname_y = f"{entityname}_y"
        # loaddata_dd_df.rename(
        #     columns={entityname_x: entityname  #, entityname_y: originalentityname
        #              },
        #     inplace=True,
        # )
        # Handle missing values for parent entities
        loaddata_dd_df["ParentEntityId"] = (
            loaddata_dd_df[cleanedentityid].replace("", pd.NA)
        )
        loaddata_dd_df["ParentEntityName"] = (
            loaddata_dd_df[cleanedentityname].replace("", pd.NA)
        )
        loaddata_dd_df["ParentEntityId"] = (
            loaddata_dd_df[cleanedentityid]
            .fillna(loaddata_dd_df[entityid])
        )
        loaddata_dd_df["ParentEntityName"] = (
            loaddata_dd_df[cleanedentityname]
            .fillna(loaddata_dd_df[entityname])
        )
        loaddata_dd_df.rename(
            columns={
                entityid: originalentityid,
                entityname: originalentityname,
                "ParentEntityId": entityid,
                "ParentEntityName": entityname,
            },
            inplace=True,
        )
        # drop unnecessary columns
        # loaddata_dd_df.drop(columns=[cleanedentityid,
        # cleanedentityname], inplace=True)
        # count of deduped records
        updatedidrecords = (loaddata_dd_df[loaddata_dd_df[entityid] !=
                                loaddata_dd_df[originalentityid]]).count()
        updatednamerecords = (loaddata_dd_df[loaddata_dd_df[entityname] !=
                                loaddata_dd_df[originalentityname]]).count()
        changednamerecords = (
            loaddata_dd_df[loaddata_dd_df[cleanedentityname] !=
                loaddata_dd_df[originalentityname]]).count()
        changedidrecords = (loaddata_dd_df[loaddata_dd_df[cleanedentityid] !=
                                loaddata_dd_df[originalentityid]]).count()
        logger.info(f"File deduplication complete, shape: {updatedidrecords}"
                    f" records updated with new {entityid} and"
                    f" {updatednamerecords} records updated"
                    f" with new {entityname}")
        logger.debug(f"File deduplication cleaned complete, "
                     f"shape: {changedidrecords}"
                     f" records updated with new {entityid} and"
                     f" {changednamerecords} records updated"
                     f" with new {entityname}")
        logger.info(f"File deduplication complete,"
                    f" shape: {loaddata_dd_df.shape}")
        return loaddata_dd_df
    else:
        # If the file hasn't been updated, use fuzzy matching for deduplication
        logger.info(f"File {map_filename} not found or unchanged,"
                    " performing fuzzy deduplication.")
        loaddata_dd_df = dedupe_entity_fuzzy(
            loaddata_dd_df, entity, threshold=threshold, output_csv=output_csv
        )
    return loaddata_dd_df


@log_function_call
def dedupe_entity_fuzzy(deupedf, entity, threshold=85, output_csv=False):
    """
    Fuzzy deduplication logic that attempts to match similar entity names.
    """
    # Log the start of the fuzzy deduplication
    logger.info("Dedupe by logic")
    originalentityname = f"Original{entity}Name"
    originalentityid = f"Original{entity}Id"
    entityname = f"{entity}Name"
    entityid = f"{entity}Id"
    cleanedentityname = f"Cleaned{entity}Name"
    cleanedentityid = f"Cleaned{entity}Id"

    # Extract entity names and IDs
    loaddata_dd_df = deupedf.copy()
    entity_names = loaddata_dd_df[[entityid, entityname]].drop_duplicates()

    # Preprocess names (lowercase and remove special characters)
    entity_names["CleanedName"] = (
        entity_names[entityname].str.lower().str.replace(r"[^a-z0-9\s]", "", regex=True)
    )

    # Create a mapping of entity names to IDs
    name_to_id = entity_names.set_index("CleanedName")[entityid].to_dict()

    # Dictionary to store potential duplicates
    potential_duplicates = defaultdict(set)

    # Apply fuzzy matching
    for cleaned_name, searchid in name_to_id.items():
        matches = process.extract(
            cleaned_name, name_to_id.keys(), scorer=fuzz.ratio, limit=5
        )
        for match_name, score, _ in matches:
            if score >= threshold and match_name != cleaned_name:
                match_id = name_to_id[match_name]
                potential_duplicates[searchid].add(match_id)
                potential_duplicates[match_id].add(searchid)

    # Convert sets to lists
    potential_duplicates = {k: list(v) for k, v in potential_duplicates.items()}

    # Save results to a CSV file if requested
    if output_csv:
        fname = f"potential_{entity.lower()}_duplicates_fname"
        potential_regentity_duplicates_filename = st.session_state[fname]
        output_df = pd.DataFrame(
            potential_duplicates.items(), columns=[entityid, "Potential Duplicates"]
        )
        output_df.to_csv(potential_regentity_duplicates_filename, index=False)

    # Create mappings for cleansed ID and Name
    id_to_cleansed = {}
    name_to_cleansed = {}

    for main_id, duplicate_ids in potential_duplicates.items():
        all_ids = [main_id] + duplicate_ids
        # Choose the smallest entityid
        cleansed_id = min(all_ids)

        # Get all names corresponding to these IDs
        matching_names = loaddata_dd_df[loaddata_dd_df[entityid].isin(all_ids)][entityname]
        cleansed_name = matching_names.value_counts().idxmax() if not matching_names.empty else pd.NA

        # Store mappings
        for searchid in all_ids:
            id_to_cleansed[searchid] = cleansed_id
            name_to_cleansed[searchid] = cleansed_name

    # Apply cleansed IDs and Names to the data
    loaddata_dd_df[cleanedentityid] = (
        loaddata_dd_df[entityid].map(id_to_cleansed).fillna(loaddata_dd_df[entityid])
    )
    loaddata_dd_df[cleanedentityname] = (
        loaddata_dd_df[entityname].map(name_to_cleansed).fillna(loaddata_dd_df[entityname])
    )

    # Rename columns to reflect the cleansed data
    loaddata_dd_df.rename(
        columns={
            entityid: originalentityid,
            entityname: originalentityname,
            cleanedentityid: entityid,
            cleanedentityname: entityname,
        },
        inplace=True,
    )
    logger.info(f"Dedupe by logic, shape: {loaddata_dd_df.shape}")
    return loaddata_dd_df