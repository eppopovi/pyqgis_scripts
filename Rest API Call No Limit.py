"""
Purpose: Retrieve GIS data from the Government of NL ArcGIS REST API MapServer website with no polygon download limit.
Script downloads data as GeoJSON and saves it to a file in a directory specified by the user (line 65).
Inputs: Edit the directory where to save file (line 65). Edit the layer_ids variable specifying which layer you want to download (line 11)
Date: Feb 07 2025
Project: NL BCA Tool
"""
import requests  # Library to send HTTP requests to a web API
import json  # Library to handle JSON data

# List of GIS layer IDs (that you can edit) to download from the Newfoundland and Labrador Land Use Atlas
# Do not overload with a lot of layers (more than 3) because this could take a lot longer than doing 3 at a time
# I FOUND IT BETTER TO DO ONE LAYER AT A TIME FOR MAX TIME EFFICIENCY!!!
layer_ids = [39, 11, 35, 28, 22, 21] #Numbers are assigned based on layer (see the link on line 8) 

# Base URL for the GIS web service API (layer ids can be found here)
base_url = "https://www.gov.nl.ca/landuseatlasmaps/rest/services/LandUseDetails/MapServer"

# Headers to mimic a real web browser request (some servers block requests without headers)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Define the maximum number of records to retrieve per request
chunk_size = 1000  # Adjust based on API limits (default ArcGIS servers often limit to 1000)

# Loop through each layer ID to retrieve its data
for layer_id in layer_ids:
    # Construct the URL for querying the specific layer
    url = f"{base_url}/{layer_id}/query"
    all_features = []  # List to store all retrieved features (spatial data)
    offset = 0  # Used for pagination to retrieve large datasets in chunks

    while True:  # Loop until all records are fetched
        # Define API query parameters
        params = {
            "where": "1=1",  # Retrieves all records (no filtering)
            "outFields": "*",  # Requests all available attributes for each record
            "f": "geojson",  # Requests data in GeoJSON format (useful for GIS applications)
            "resultOffset": offset,  # Starts retrieving records from this index (pagination)
            "resultRecordCount": chunk_size  # Number of records to retrieve per request
        }

        # Send HTTP GET request to the API with parameters
        response = requests.get(url, params=params, headers=headers)
        
        # Check if the request was successful (HTTP 200 OK)
        if response.status_code == 200:
            data = response.json()  # Convert response to JSON format
            features = data.get("features", [])  # Extract 'features' list (geospatial records)

            if not features:
                break  # Exit loop if no more records are returned

            all_features.extend(features)  # Add retrieved records to the list
            offset += chunk_size  # Move to the next batch of records
        else:
            # Print error message if the request fails
            print(f"Error fetching layer {layer_id}: {response.status_code} - {response.text}")
            break  # Stop retrieving data if an error occurs

    # If records were retrieved, save them to a file
    if all_features:
        geojson_output = {
            "type": "FeatureCollection",  # Standard GeoJSON structure
            "features": all_features  # Include all retrieved records
        }

        # Define file path for saving data
        save_path = f"C:/Users/Heron/Downloads/landuse_layer_{layer_id}.geojson"
        
        # Write GeoJSON data to file
        with open(save_path, "w", encoding="utf-8") as file:
            json.dump(geojson_output, file, ensure_ascii=False, indent=4)
        
        print(f"Data saved: {save_path}")  # Confirm successful save
    else:
        print(f"No data retrieved for layer {layer_id}")  # Notify if no data was found

print("Done")  # Print final message when script completes
