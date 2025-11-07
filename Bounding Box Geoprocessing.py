"""
Purpose: 
This script processes vector data files (e.g., Shapefile, GeoPackage, GeoJSON) to 
create minimum oriented bounding rectangles (OBBs) for each feature within those files. 
It takes input files from a folder, processes each file to generate oriented bounding rectangles, 
and saves the results in an output folder.

Inputs:
- `input_folder`: Folder containing the input vector data files (line 82).
- `output_folder`: Folder where the processed oriented bounding rectangles will be saved (line 83).

Date: February 7, 2025
Project: NL BCA Tool
"""

import os
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsProcessingFeedback,
    QgsProcessingFeatureSourceDefinition
)
from qgis.analysis import QgsNativeAlgorithms
import processing

# Function to create oriented minimum bounding rectangles
def create_oriented_bounding_rectangles(input_folder, output_folder):
    """
    This function processes vector data files to create minimum oriented bounding rectangles (OBBs)
    and saves them to the specified output folder.
    
    Parameters:
        input_folder (str): The folder containing the input vector files.
        output_folder (str): The folder where the output files will be saved.
    """
    
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize QGIS processing framework and add the native algorithms provider
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    # Iterate through all files in the input folder
    for file_name in os.listdir(input_folder):
        # Process only valid vector files (.shp, .gpkg, .geojson)
        if file_name.endswith(".shp") or file_name.endswith(".gpkg") or file_name.endswith(".geojson"):
            # Construct the full path of the input file
            input_path = os.path.join(input_folder, file_name)
            
            # Load the vector layer from the input file
            layer = QgsVectorLayer(input_path, file_name, "ogr")

            # Check if the layer is valid
            if not layer.isValid():
                print(f"Invalid layer: {file_name}")
                continue  # Skip the file if it's invalid

            print(f"Processing oriented bounding rectangles for: {file_name}")

            # Define the output file name and path
            output_file_name = f"oriented_bounding_rectangles_{file_name}"
            output_path = os.path.join(output_folder, output_file_name)

            # Set parameters for the processing tool (native:orientedminimumboundingbox)
            processing_params = {
                'INPUT': QgsProcessingFeatureSourceDefinition(input_path, selectedFeaturesOnly=False),
                'OUTPUT': output_path
            }

            feedback = QgsProcessingFeedback()

            try:
                # Run the "Minimum Oriented Bounding Box" tool using the specified parameters
                processing.run("native:orientedminimumboundingbox", processing_params, feedback=feedback)
                print(f"Oriented bounding rectangles saved to: {output_path}")
            except Exception as e:
                # Handle errors that may occur during processing
                print(f"Error processing {file_name}: {e}")

# Define input and output folders for the user to modify
input_folder = r"C:\Users\Heron\Desktop\Clipped\Segmentation\Fix Geo"
output_folder = r"C:\Users\Heron\Desktop\Clipped\Segmentation\Minimal Bounding Geo"

# Run the script by calling the function with the defined input and output folders
create_oriented_bounding_rectangles(input_folder, output_folder)

