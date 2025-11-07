"""
Purpose: 
This script is designed to save temporary layers from a QGIS project as GeoPackage (.gpkg) files to a specified directory. Each layer is assigned a unique name and stored in the specified location.

Inputs: 
1. `save_dir` (Line 17): Directory path where the GeoPackage files will be saved. Modify this to the desired folder location on your system.
2. `temp_layer_counter` (Line 20): A starting integer used to generate unique names for the temporary layers. Modify this if needed.
3. QGIS Project: The script loops through all layers in the current QGIS project, so you need an open project with temporary layers.
4. layer.name "Background" saves as Background(#) where # is the temp_layer_counter (line 22)
Date: February 7, 2025
Project: NL BCA Tool
"""

import os

# Define the directory where you want to save the layers
save_dir = r"C:\Users\Heron\Desktop\Clipped\Segmentation"  # Change this to your desired location

# Loop through all layers in the current QGIS project
temp_layer_counter = 114  # Initialize a counter to create unique names
for layer in QgsProject.instance().mapLayers().values():
    if layer.isTemporary() and layer.name() != "Background":
        # Generate a unique name for each temporary layer
        layer_name = f"temp_layer_{temp_layer_counter}"
        file_path = os.path.join(save_dir, f"{layer_name}.gpkg")  # Save as GeoPackage

        # Save the layer to the specified directory as a .gpkg file
        QgsVectorFileWriter.writeAsVectorFormat(layer, file_path, "utf-8", layer.crs(), "GPKG")

        print(f"Saved {layer_name} to {file_path}")
        
        # Increment the counter to ensure unique names for each layer
        temp_layer_counter += 1
