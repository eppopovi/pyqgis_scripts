"""
Purpose: 
This script is designed to merge multiple vector layers (e.g., shapefiles, GeoPackages, or GeoJSON files)
from a specified input folder and save the merged result in an output folder. It is useful for combining
spatial data that has been clipped or segmented into a single layer, while ensuring that the Coordinate Reference
System (CRS) remains consistent with the project's CRS.

Inputs:
- input_folder (Line 75): Directory containing the vector layers (e.g., shapefiles, GeoPackages, or GeoJSON files).
  Modify this variable to specify the folder from which layers will be loaded.
- output_folder (Line 76): Directory where the merged layer will be saved. Modify this variable to specify the desired output folder.
- output_file_name (Line 77): The name for the merged output file (e.g., "merged_bounding_boxes.gpkg"). 
  Modify this variable to set the desired name for the merged layer.

Date: February 7, 2025
Project: NL BCA Tool
"""

import os
from qgis.core import (
    QgsApplication,
    QgsProcessingFeedback,
    QgsProject
)
from qgis.analysis import QgsNativeAlgorithms
import processing

# Function to merge bounding box geometry layers
def merge_layers(input_folder, output_folder, output_file_name):
    # Check if the output folder exists, create it if it doesn't
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize the QGIS processing framework to use its tools
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    # Gather all vector layers (shapefiles, GeoPackages, and GeoJSON files) from the input folder
    input_layers = []
    for file_name in os.listdir(input_folder):
        # Check if the file is a valid vector file type
        if file_name.endswith(".shp") or file_name.endswith(".gpkg") or file_name.endswith(".geojson"):
            input_path = os.path.join(input_folder, file_name)
            input_layers.append(input_path)  # Add the file path to the input layers list

    # If no valid layers are found, print an error and stop the process
    if not input_layers:
        print("No valid vector layers found in the input folder.")
        return

    # Print the number of layers found to merge
    print(f"Merging {len(input_layers)} layers from {input_folder}")

    # Define the output path for the merged layer
    output_path = os.path.join(output_folder, output_file_name)

    # Set up the parameters for the merge operation
    processing_params = {
        'LAYERS': input_layers,  # List of input layers to be merged
        'CRS': QgsProject.instance().crs().toWkt(),  # Use the project's CRS to ensure consistency
        'OUTPUT': output_path  # Path where the merged layer will be saved
    }

    # Create a feedback object for monitoring the process
    feedback = QgsProcessingFeedback()

    try:
        # Run the "Merge Vector Layers" processing tool with the specified parameters
        processing.run("native:mergevectorlayers", processing_params, feedback=feedback)
        print(f"Merged layer saved to: {output_path}")
    except Exception as e:
        # If an error occurs during the merging process, print the error
        print(f"Error merging layers: {e}")

# Define input and output folders, and the output file name
input_folder = r"C:\Users\Heron\Desktop\Clipped\Segmentation\Minimal Bounding Geo"  # Modify input folder here
output_folder = r"C:\Users\Heron\Desktop\Clipped\Segmentation\Merged Bounding Boxes"  # Modify output folder here
output_file_name = "merged_bounding_boxes.gpkg"  # Modify output file name here

# Run the function to merge the layers
merge_layers(input_folder, output_folder, output_file_name)
