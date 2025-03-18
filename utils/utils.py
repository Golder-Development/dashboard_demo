from utils.logger import datapipeline_logger as logger, log_function_call
import os
import csv
import zipfile
import io
import re
import ast
import pandas as pd
import time
import tqdm
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import GoogleV3
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import spacy

# attach tqdm to pandas
tqdm.pandas

# Download necessary NLTK resources (if you haven't already)
nltk.download('stopwords')
nltk.download('wordnet')

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the geolocator
# Load the API key from an environment variable
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise RuntimeError("Google API key not found. Please set "
                       "the GOOGLE_API_KEY environment variable.")

geolocator = GoogleV3(api_key=api_key)


@log_function_call(logger)
def checkdirectory():
    current_dir = os.getcwd()
    current_dir

    # check current directory contains the file README.md
    if os.path.exists("README.md"):
        print("The file README.md exists in the current directory")
    else:
        print("The file README.md does not exist in the current directory")
        print("You are in the directory: ", current_dir)
        print("Changing current directory to its parent directory")
        os.chdir(os.path.dirname(current_dir))
        print("You set a new current directory")
        current_dir = os.getcwd()
        if os.path.exists("README.md"):
            print("The file README.md exists in the current directory")
        else:
            RuntimeError("The file README.md does not exist in the"
                         " current directory, please"
                         " check the current directory")
            print("Current Directory =", current_dir)


@log_function_call(logger)
def save_dataframe_to_zip(df, zip_filename, csv_filename='data.csv'):
    logger.info(f"Saving Df to {zip_filename}")
    """Saves a pandas DataFrame to a zipped CSV file.

    Args:
        df: The pandas DataFrame to save.
        zip_filename: The name of the zip file to create.
        csv_filename: The name of the CSV file inside the zip archive.
    """
    # save the dataframe to a csv file
    df.to_csv(csv_filename, index=False)
    # Create an in-memory buffer for the CSV data
    csv_buffer = io.StringIO()
    # Save the DataFrame to the buffer as a CSV
    df.to_csv(csv_buffer,
              index=True,
              index_label="index",
              quoting=csv.QUOTE_NONNUMERIC
              )  # index=False to exclude the index
    # Create a zip file and add the CSV data to it
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(csv_filename, csv_buffer.getvalue())


@log_function_call(logger)
def separate_string(input_string):
    # Extract the contents of the brackets
    bracket_content = re.search(r'\((.*?)\)', input_string).group(1)
    # Extract the remaining text excluding the
    # brackets and the hyphen or minus sign
    remaining_text = re.sub(r'\(.*?\)| -', '', input_string).strip()
    return remaining_text, bracket_content


@log_function_call(logger)
def clean_text(text):
    """Cleans the input text."""
    # check that passed text is a string
    if not isinstance(text, str):
        return ""  # Return empty string for non-string input
    # Remove HTML tags (if any)
    text = re.sub(r'<.*?>', '', text)
    # Remove special characters and punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenization and stop word removal
    words = text.split()
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    # Rejoin the cleaned words
    cleaned_text = ' '.join(words)
    # return the cleaned text
    return cleaned_text


# Sentiment analysis on the cleaned text:
def get_sentiment(text):
    # check that passed text is a string
    if isinstance(text, str):
        # turn into a TextBlob object
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity
    else:
        return None, None


# Functions to categorize the polarity and subjectivity scores
def categorize_polarity(polarity):
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'


def categorize_subjectivity(subjectivity):
    if subjectivity > 0.8:
        return 'highly subjective'
    elif subjectivity > 0.6:
        return 'subjective'
    elif subjectivity > 0.4:
        return 'neutral'
    elif subjectivity > 0.2:
        return 'objective'
    else:
        return 'higly objective'


# covert a string to a list
def string_to_list(location_str):
    """Safely converts a string representation of a list to a list."""
    try:
        return ast.literal_eval(location_str)
    except (ValueError, SyntaxError, TypeError):
        return []


@log_function_call(logger)
def restrict_api_key_server(project_id: str, key_id: str) -> Key:
    """
    Restricts the API key based on IP addresses. You can specify one or
    more IP addresses of the callers,
    for example web servers or cron jobs, that are allowed to use your API key.

    TODO(Developer): Replace the variables before running this sample.

    Args:
        project_id: Google Cloud project id.
        key_id: ID of the key to restrict. This ID is auto-created
        during key creation.
            This is different from the key string. To obtain the key_id,
            you can also use the lookup api: client.lookup_key()

    Returns:
        response: Returns the updated API Key.
    """

    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    # Restrict the API key usage by specifying the IP addresses.
    # You can specify the IP addresses in IPv4 or IPv6 or a
    # subnet using CIDR notation.
    server_key_restrictions = api_keys_v2.ServerKeyRestrictions()
    server_key_restrictions.allowed_ips = ["80.189.63.110"]

    # Set the API restriction.
    # For more information on API key restriction, see:
    # https://cloud.google.com/docs/authentication/api-keys
    restrictions = api_keys_v2.Restrictions()
    restrictions.server_key_restrictions = server_key_restrictions

    key = api_keys_v2.Key()
    key.name = f"projects/{project_id}/locations/global/keys/{key_id}"
    key.restrictions = restrictions

    # Initialize request and set arguments.
    request = api_keys_v2.UpdateKeyRequest()
    request.key = key
    request.update_mask = "restrictions"

    # Make the request and wait for the operation to complete.
    response = client.update_key(request=request).result()

    print(f"Successfully updated the API key: {response.name}")
    # Use response.key_string to authenticate.
    return response


# define media types
def classify_media(text):
    media_dict = {'video': ['video', 'watch', 'live',
                            'stream', 'youtube',
                            'vimeo', 'twitch'],
                  'audio': ['audio', 'listen', 'podcast', 'radio'],
                  'image': ['image', 'photo', 'picture', 'gif'],
                  'infographic': ['infographic'],
                  'poll': ['poll'],
                  'twitter': ['twitter', 'X', 'x', 'tweet', 'retweeted'],
                  'facebook': ['facebook', 'fb', 'like', 'share', 'comment'],
                  'instagram': ['instagram', 'ig', ],
                  'linkedin': ['linkedin', 'share'],
                  }
    # Handle NaN cases safely
    if pd.isna(text):
        return 'text'
    for key, value in media_dict.items():
        # Lowercase to ensure case insensitivity
        if any(word in text.lower() for word in value):
            return key
    # Default to 'text' if no media type is found
    return 'text'


# Function to get geolocation information
@log_function_call(logger)
def get_geolocation_info(location):
    usetimedelay = True
    try:
        location_info = geolocator.geocode(location, timeout=10)
        if location_info:
            if usetimedelay:
                time.sleep(1)
            return {
                'latitude': location_info.latitude,
                'longitude': location_info.longitude,
                'address': location_info.address
            }
        else:
            if usetimedelay:
                time.sleep(1)
            return {
                'latitude': None,
                'longitude': None,
                'address': None
            }
    except GeocoderTimedOut:
        print(location)
        if usetimedelay:
            time.sleep(1)
        return {
            'latitude': None,
            'longitude': None,
            'address': None
        }
    except Exception as e:
        print(f"Geocoding error: {e}")
        if usetimedelay:
            time.sleep(1)
        return {
            'latitude': None,
            'longitude': None,
            'address': None
        }


# Function to extract geolocation details
@log_function_call(logger)
def extract_geolocation_details(address):
    if address:
        address_parts = address.split(', ')
        country = address_parts[-1] if len(address_parts) > 0 else None
        state = address_parts[-2] if len(address_parts) > 1 else None
        continent = address_parts[-3] if len(address_parts) > 2 else None
        return continent, country, state
    else:
        return None, None, None


@log_function_call(logger)
def extract_locations(text, keyword_processor, nlp):
    """Extracts location names from text using NLP and predefined list."""
    logger.debug("Starting location extraction...")
    # convert text to string
    text = str(text)
    # Use NLP to extract geographic locations (GPE entities)
    doc = nlp(text)
    nlp_locations = (
        {ent.text.lower() for ent in doc.ents if ent.label_ == "GPE"})
    logger.debug(f"NLP Extracted Locations: {nlp_locations}")

    # Fast keyword matching for known locations
    matched_locations = (
        set(keyword_processor.extract_keywords(text.lower())))
    logger.debug("Matched Locations"
                 f" from Predefined List: {matched_locations}")

    # Return matched locations if found; otherwise,
    # return NLP-extracted ones
    final_locations = (
        matched_locations if matched_locations else nlp_locations)
    logger.debug(f"Final Extracted Locations: {final_locations}")

    return list(final_locations)
