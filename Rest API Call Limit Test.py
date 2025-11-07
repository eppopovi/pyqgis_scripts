"""
Purpose: Retrieve GIS data from the Government of NL ArcGIS REST API MapServer website with 2000 polygon download limit. 
Script downloads data as GeoJSON and saves it to a file in a directory specified by the user (line 44).
Inputs: Edit the directory where to save file (line 44). Edit the layer_ids variable specifying which layer you want to download (line 11)
Date: Feb 07 2025
Project: NL BCA Tool
"""

# Import the `requests` library, which is used for making HTTP requests to access web services (in this case, an API).
import requests

# List of layer IDs to fetch data from. Each number corresponds to a specific layer in the GIS data service.
# Do not overload with a lot of layers (more than 3) because this could take a lot longer than doing 3 at a time
# I FOUND IT BETTER TO DO ONE LAYER AT A TIME FOR MAX TIME EFFICIENCY!!!
layer_ids = [40]  # In this case, the script will only request layer 40, but you could add more IDs if needed.

# Base URL for the ArcGIS REST API service from which data will be fetched.
base_url = "https://www.gov.nl.ca/landuseatlasmaps/rest/services/LandUseDetails/MapServer"

# Headers to be sent with the HTTP request. The 'User-Agent' field is commonly included to indicate the client (your script).
# This makes the request look more like a typical web browser request, which some servers require.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Iterate over each layer ID provided in the list `layer_ids`.
for layer_id in layer_ids:
    # Build the URL for making the API call to the ArcGIS service, targeting a specific layer (e.g., layer 40).
    url = f"{base_url}/{layer_id}/query"  # This constructs the full URL to access the data for layer 40.

    # Parameters for the query request. 
    # "where" specifies the condition for which records to retrieve, "1=1" means all records are selected (no filtering).
    # "outFields" specifies which fields to include in the response, "*" means all fields.
    # "f" specifies the format of the response, here it is "geojson" for geospatial data in GeoJSON format.
    params = {
        "where": "1=1",  # Select all records.
        "outFields": "*",  # Include all fields of data.
        "f": "geojson"  # Request data in GeoJSON format.
    }
    
    # Make an HTTP GET request to the server using the URL and parameters.
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful by looking at the status code returned by the server.
    if response.status_code == 200:
        # If the request was successful (status code 200), save the returned data (GeoJSON) to a file.
        
        # Construct a file path where the data will be saved. The file will be named based on the layer ID.
        save_path = f"C:/Users/Heron/Downloads/landuse_layer_{layer_id}.geojson"
        
        # Open the file in write mode, using UTF-8 encoding to ensure the data is saved correctly.
        with open(save_path, "w", encoding="utf-8") as file:
            # Write the content (GeoJSON data) of the response into the file.
            file.write(response.text)
        
        # Print a message confirming that the data has been saved successfully.
        print(f"Data saved: {save_path}")
    else:
        # If the request failed (status code other than 200), print an error message with details.
        print(f"Error fetching layer {layer_id}: {response.status_code} - {response.text}")

# After processing all layers, print "Done" to indicate that the script has completed.
print("Done")
