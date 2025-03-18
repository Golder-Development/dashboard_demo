# Function to get geolocation information
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
def extract_geolocation_details(address):
    if address:
        address_parts = address.split(', ')
        country = address_parts[-1] if len(address_parts) > 0 else None
        state = address_parts[-2] if len(address_parts) > 1 else None
        continent = address_parts[-3] if len(address_parts) > 2 else None
        return continent, country, state
    else:
        return None, None, None


def extract_locations(text, keyword_processor):
    """Extracts location names from text using NLP and predefined list."""
    if keyword_processor is None:
        logger.info("Keyword processor is not initialized.")
        keyword_processor = KeywordProcessor()

    logging.debug("Starting location extraction...")
    # convert text to string
    text = str(text)
    # Use NLP to extract geographic locations (GPE entities)
    doc = nlp(text)
    nlp_locations = (
        {ent.text.lower() for ent in doc.ents if ent.label_ == "GPE"})
    logging.debug(f"NLP Extracted Locations: {nlp_locations}")

    # Fast keyword matching for known locations
    matched_locations = (
        set(keyword_processor.extract_keywords(text.lower())))
    logging.debug("Matched Locations"
                    f" from Predefined List: {matched_locations}")

    # Return matched locations if found; otherwise,
    # return NLP-extracted ones
    final_locations = (
        matched_locations if matched_locations else nlp_locations)
    logging.info(f"Final Extracted Locations: {final_locations}")

    return list(final_locations)

def find_location_match(location, worldcities_df):
    """
    Search for a location in multiple columns of worldcities_df.

    Args:
        location (str): The location to search for.
        worldcities_df (DataFrame): The dataframe containing city data.

    Returns:
        dict: A dictionary containing the matched value, the column it was
        found in, latitude, longitude, and country.
              Returns None if no match is found.
    """
    search_columns = ['city', 'city_ascii', 'country',
                      'iso2', 'iso3', 'admin_name']

    # Convert input to string and lowercase for case-insensitive comparison
    location = str(location).strip().lower()

    for col in search_columns:
        # Find rows where the location matches the column
        match = worldcities_df[worldcities_df[col]
                               .astype(str)
                               .str.strip()
                               .str.lower() == location]

        if not match.empty:
            # Extract the first match found
            result = {
                'matched_value': match.iloc[0][col],
                'matched_column': col,
                'latitude': match.iloc[0]['lat'],
                'longitude': match.iloc[0]['lng'],
                'country': match.iloc[0]['country']
            }
            return result

    return None  # Return None if no match is found