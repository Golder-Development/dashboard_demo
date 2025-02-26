import pandas as pd
import streamlit as st
import os
from rapidfuzz import process, fuzz
from collections import defaultdict


def dedupe_entity_file(loaddata_dd_df,
                       entity,
                       map_filename,
                       threshold=85,
                       output_csv=False):
    """
    loads a dedupe mapping file from reference folder and
    merges it with the original data.  Merges on field named
    {entity]id creates new columns original{entity}id and
    original{entity}name - new data is returned in a dataframe
    called loaddata_dd_df.  If the file does not exist, the
    dedupe_entity_fuzzy function is called to dedupe the data
    and return the new data in loaddata_dd_df
    """
    # Load the data
    ref_dir = st.session_state.directories["reference_dir"]
    originalentityname = f"Original{entity}Name"
    originalentityid = f"Original{entity}Id"
    entityname = f"{entity}Name"
    entityid = f"{entity}Id"
    cleanedentityname = f"Cleaned{entity}Name"
    cleanedentityid = f"Cleaned{entity}Id"
    # check that reentity_deduped file exists using global variables
    if map_filename not in st.session_state.filenames:
        raise ValueError(f"{map_filename} not found"
                         " in session state filenames")
    else:
        # check that join on field exists in the data
        if entityid not in loaddata_dd_df.columns:
            raise ValueError(f"{entityid} not found in data")
    # check that file exists at identified path from global var
    if os.path.exists(os.path.join(ref_dir,
                                   st.session_state
                                   .filenames[map_filename])):
        # load regentity_map_fname file using global variables
        dedupedfilename = (
            st.session_state.filenames[map_filename])
        dedupedfilepath = os.path.join(ref_dir, dedupedfilename)
        re_dedupe_df = pd.read_csv(dedupedfilepath)
        # merge re_dedupe_df with original data
        loaddata_dd_df = pd.merge(loaddata_dd_df,
                                  re_dedupe_df,
                                  how='left',
                                  on=entityid)
        # rename RegulatedEntityName_x to RegulatedEntityName
        # and RegulatedEntityName_y to OriginalRegulatedEntityName
        entityname_x = f"{entityname}_x"
        entityname_y = f"{entityname}_y"
        loaddata_dd_df.rename(
            columns={entityname_x: entityname,
                     entityname_y: originalentityname
                     }, inplace=True)
        # use the RegulatedEntityId and RegulatedEntityName columns
        # to update the original data with new columns called
        # parententityid and parententityname - in no match exists
        # the original data will be used

        loaddata_dd_df['ParentEntityId'] = (
            loaddata_dd_df[cleanedentityid].replace("", pd.NA)
        )
        loaddata_dd_df['ParentEntityName'] = (
            loaddata_dd_df[cleanedentityname].replace("", pd.NA)
        )
        loaddata_dd_df['ParentEntityId'] = (
            loaddata_dd_df['ParentEntityId']
            .fillna(loaddata_dd_df[entityid])
        )
        loaddata_dd_df['ParentEntityName'] = (
            loaddata_dd_df['ParentEntityName']
            .fillna(loaddata_dd_df[entityname])
        )
        loaddata_dd_df.rename(
            columns={entityid: originalentityid,
                     entityname: originalentityname,
                     "ParentEntityId": entityid,
                     "ParentEntityName": entityname},
            inplace=True)
        return loaddata_dd_df
    else:
        # Run dedupe logic if file does not exist
        loaddata_dd_df = dedupe_entity_fuzzy(loaddata_dd_df,
                                             entity,
                                             threshold=85,
                                             output_csv=output_csv)
    return loaddata_dd_df


def dedupe_entity_fuzzy(deupedf, entity, threshold=85, output_csv=False):
    # Load the data
    output_dir = st.session_state.directories["output_dir"]

    originalentityname = f"Original{entity}Name"
    originalentityid = f"Original{entity}Id"
    entityname = f"{entity}Name"
    entityid = f"{entity}Id"
    cleanedentityname = f"Cleaned{entity}Name"
    cleanedentityid = f"Cleaned{entity}Id"
    # Extract donor names and IDs
    loaddata_dd_df = deupedf.copy()
    entity_names = (
        loaddata_dd_df[[entityid,
                        entityname]].drop_duplicates()
        )

    # Preprocess names (lowercase and remove special characters)
    entity_names["CleanedName"] = (
        entity_names[entityname]
        .str.lower()
        .str.replace(r"[^a-z0-9\s]", "", regex=True)
        )

    # Create a mapping of donor names to IDs
    name_to_id = (
        entity_names.set_index("CleanedName")[entityid].to_dict()
    )

    # Dictionary to store potential duplicates
    potential_duplicates = defaultdict(set)

    # Apply fuzzy matching
    for cleaned_name, entityid in name_to_id.items():
        matches = process.extract(cleaned_name,
                                  name_to_id.keys(),
                                  scorer=fuzz.ratio,
                                  limit=5)
        for match_name, score, _ in matches:
            if score >= threshold and match_name != cleaned_name:
                match_id = name_to_id[match_name]
                potential_duplicates[entityid].add(match_id)
                potential_duplicates[match_id].add(entityid)

    # Convert sets to lists
    potential_duplicates = {k: list(v) for k,
                            v in potential_duplicates.items()}

    # Save results to a CSV file
    fname = f"potential_{entity}_duplicates_fname"
    if output_csv:
        potential_regentity_duplicates_filemane = (
            st.session_state
            .filenames[fname]
        )
        potential_regentity_duplicates_filemane = (
            os.path.join(output_dir,
                         potential_regentity_duplicates_filemane)
        )
        output_df = (
            pd.DataFrame(potential_duplicates.items(),
                         columns=[entityid,
                         "Potential Duplicates"])
            )

        output_df.to_csv(potential_regentity_duplicates_filemane,
                         index=False)

    # Create mappings for cleansed ID and Name
    id_to_cleansed = {}
    name_to_cleansed = {}

    for main_id, duplicate_ids in potential_duplicates.items():
        all_ids = [main_id] + duplicate_ids
        # Choose the smallest entityid
        cleansed_id = min(all_ids)

        # Get all names corresponding to these IDs
        matching_names = (
            loaddata_dd_df[loaddata_dd_df[entityid].isin(all_ids)][entityname]
        )

        # Choose the most frequent name
        cleansed_name = matching_names.value_counts().idxmax()

        # Store mappings
        for entityid in all_ids:
            id_to_cleansed[entityid] = cleansed_id
            name_to_cleansed[entityid] = cleansed_name

    # convert Id = "" to null
    loaddata_dd_df[entityid] = (
        loaddata_dd_df[entityid].replace("", pd.NA)
    )
    # Apply mappings to the dataset
    loaddata_dd_df[cleanedentityid] = (
        loaddata_dd_df[entityid]
        .map(id_to_cleansed)
        .fillna(loaddata_dd_df[entityid])
        )
    loaddata_dd_df[cleanedentityname] = (
        loaddata_dd_df[entityname]
        .map(name_to_cleansed)
        .fillna(loaddata_dd_df[entityname])
        )

    # rename Cleansed ID to Id and Cleansed Name to Name
    loaddata_dd_df.rename(
        columns={entityid: originalentityid,
                 entityname: originalentityname,
                 cleanedentityid: entityid,
                 cleanedentityname: entityname},
        inplace=True
        )
    return loaddata_dd_df
