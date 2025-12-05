"""
# Purpose: This script is designed to count and display the number of temporary layers in a QGIS project.
# Inputs: The user can modify the code to run in a QGIS environment, where it loops through the map layers and counts the temporary layers.
# Date: February 7, 2025
# Project: NL BCA Tool
"""

# Initialize a counter for temporary layers
temp_layer_count = 0

# Loop through all layers in the current QGIS project
for layer in QgsProject.instance().mapLayers().values():
    if layer.isTemporary():
        # Increment the counter for each temporary layer
        temp_layer_count += 1

# Print the total number of temporary layers
print(f"Number of temporary layers: {temp_layer_count}")



"""
Purpose: 
This script is designed to iterate through all layers in a QGIS project and save any temporary layers as GeoPackage (.gpkg) files. 
The user can modify the directory where the files are saved and adjust the number of layers processed.

Inputs: 
- User should modify the `save_dir` (line 17) to specify the directory where the GeoPackage files will be stored.
- The script processes layers in the current QGIS project.

Date: February 7, 2025
Project: NL BCA Tool
"""

import os

# Define the directory where you want to save the layers
save_dir = r"C:\Users\Heron\Desktop\Clipped\Segmentation"  # Change this to your desired location

# Loop through all layers in the current QGIS project
temp_layer_counter = 1  # Initialize a counter to create unique names
for layer in QgsProject.instance().mapLayers().values():
    # Check if the layer is a temporary layer
    if layer.isTemporary():
        # Generate a unique name for each temporary layer
        layer_name = f"temp_layer_{temp_layer_counter}"
        
        # Define the file path to save the layer as a GeoPackage file
        file_path = os.path.join(save_dir, f"{layer_name}.gpkg")  # Save as GeoPackage

        # Save the layer to the specified directory as a .gpkg file using the QgsVectorFileWriter
        QgsVectorFileWriter.writeAsVectorFormat(layer, file_path, "utf-8", layer.crs(), "GPKG")

        # Print confirmation that the layer has been saved
        print(f"Saved {layer_name} to {file_path}")
        
        # Increment the counter to ensure unique names for each layer
        temp_layer_counter += 1
