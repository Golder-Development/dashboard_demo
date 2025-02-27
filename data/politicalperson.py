from utils.logger import logger
from utils.decorators import log_function_call  # Import decorator


def map_mp_to_party():
    # if ListOfPoliticalPeople_Final.csv file does not exist:
    #     # import ListOfPoliticalPeople_Final.csv file
    #     BASE_DIR = st.session_state.BASE_DIR
    #     politician_party_filename = st.session_state.politician_party_fname
    #     politician_party_filepath = os.path.join(BASE_DIR,
    # politician_party_filename)
    #     politician_party_df = pd.read_csv(politician_party_filepath)
    #     # merge ListOfPoliticalPeople_Final.csv file with original data
    #     loaddata_df = pd.merge(df, politician_party_df, how='left',
    # on='RegulatedEntityID')
    #     # update blank PartyName to "Unidentified Party"
    #     loaddata_df['PartyName'] = loaddata_df['PartyName'].replace("",
    # RegulatedEntityName)
    #     # update blank PartyId to "1000001"
    #     loaddata_df['PartyId'] = loaddata_df['PartyId'].replace("",
    # RegulatedEntityId)
    #     # update blank PoliticianName to "Unidentified Politician"
    #     loaddata_df['PoliticianName'] = loaddata_df['PoliticianName']
    # .replace("", "Unidentified Politician")
    #     # update blank PoliticianId to "1000001"
    #     loaddata_df['PoliticianId'] = loaddata_df['PoliticianId'].replace("",
    # "1000001")

    return
