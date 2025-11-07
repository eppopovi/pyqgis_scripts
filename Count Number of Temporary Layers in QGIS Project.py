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
