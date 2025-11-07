"""
Purpose:
This script processes vector layers (GeoPackage files) from a specified input folder,
fixes any invalid geometries using QGIS's "Fix Geometries" tool, and saves the fixed layers
to an output folder. This is useful for cleaning up spatial data that may have errors like
invalid geometries or topological issues. The script assumes the input files are GeoPackage 
files (.gpkg) and outputs the fixed layers in the same format.

Inputs:
1. `input_folder` (Line 96): Path to the folder containing the input GeoPackage files (.gpkg).
   Modify this to specify where your input data is stored.
2. `output_folder` (Line 97): Path to the folder where the fixed layers will be saved.
   Modify this to specify where you want the output to go.

Outputs:
The script will output fixed vector layers (GeoPackage files) to the `output_folder` specified.
Each layer will be saved with the same filename as the input, but with geometries fixed.

Date: February 7, 2025
Project: NL BCA Tool
"""

import os
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsProcessingFeedback,
    QgsProcessing,
    QgsProject,
    QgsVectorFileWriter
)
from qgis.analysis import QgsNativeAlgorithms

# Function to process layers and fix geometries
def fix_geometries(input_folder, output_folder):
    # Check if the output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize QGIS processing framework and register native algorithms
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    # Iterate through all files in the input folder
    for file_name in os.listdir(input_folder):
        # Check if the file is a GeoPackage (.gpkg)
        if file_name.endswith(".gpkg"):
            # Build the full file path for the input file
            input_path = os.path.join(input_folder, file_name)
            
            # Load the vector layer using the file path
            layer = QgsVectorLayer(input_path, file_name, "ogr")

            # Check if the layer is valid (i.e., if it was successfully loaded)
            if not layer.isValid():
                print(f"Invalid layer: {file_name}")
                continue  # Skip this file and move on to the next

            print(f"Processing: {file_name}")

            # Define processing parameters for the "Fix Geometries" tool
            processing_params = {
                'INPUT': layer,  # Input layer
                'OUTPUT': 'memory:'  # Temporary layer to store fixed geometries in memory
            }

            # Initialize feedback object to monitor the progress of processing
            feedback = QgsProcessingFeedback()

            try:
                # Run the "Fix Geometries" tool to correct invalid geometries
                result = processing.run("native:fixgeometries", processing_params, feedback=feedback)
                fixed_layer = result['OUTPUT']  # The fixed layer is returned as output

                # Check if the fixed layer has any features (if any changes were made)
                if fixed_layer and fixed_layer.featureCount() > 0:
                    # Define the output path for the fixed layer
                    output_path = os.path.join(output_folder, file_name)
                    
                    # Write the fixed layer to the output folder as a GeoPackage
                    QgsVectorFileWriter.writeAsVectorFormat(
                        fixed_layer,
                        output_path,
                        "utf-8",  # Encoding for the output file
                        layer.crs(),  # Coordinate reference system of the original layer
                        "GPKG"  # Output format (GeoPackage)
                    )
                    print(f"Fixed geometries saved to: {output_path}")
                else:
                    print(f"No geometries were fixed for: {file_name}")

            except Exception as e:
                # Catch any errors that occur during processing and display a message
                print(f"Error processing {file_name}: {e}")

# Define the input and output folder paths
input_folder = r"C:\Users\Heron\Desktop\QGIS\NL BCA Building Segmentation\Boundaries\NL Municipal Boundaries\Municipal Boundaries Split"
output_folder = r"C:\Users\Heron\Desktop\QGIS\NL BCA Building Segmentation\Boundaries\NL Municipal Boundaries\Municipal Boundaries Split Fix Geo"

# Run the function to process the geometries
fix_geometries(input_folder, output_folder)
