"""
Purpose: 
Script reprojects all vector layers (GeoPackage files) from a given input folder into a new Coordinate Reference System (CRS), specifically Web Mercator (EPSG:3857). It saves the reprojected layers into a specified output folder.

Inputs: 
- Line 83: `input_folder`: Path to the folder containing the GeoPackage files to be reprojected. Modify this path as needed.
- Line 84: `output_folder`: Path to the folder where the reprojected layers will be saved. Modify this path as needed.

Date: February 7, 2025

Project: 
NL BCA Tool
"""

import os
from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsProcessingFeedback,
    QgsVectorFileWriter
)
from qgis.analysis import QgsNativeAlgorithms
import processing

# Function to reproject layers using the "native:reprojectlayer" tool
def reproject_layers(input_folder, output_folder):
    # Step 1: Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Step 2: Initialize the QGIS processing framework by adding the native algorithms provider
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    # Step 3: Iterate through all files in the input folder
    for file_name in os.listdir(input_folder):
        # Step 4: Process only GeoPackage files
        if file_name.endswith(".gpkg"):
            input_path = os.path.join(input_folder, file_name)
            layer = QgsVectorLayer(input_path, file_name, "ogr")  # Load the vector layer

            # Step 5: Check if the layer is valid
            if not layer.isValid():
                print(f"Invalid layer: {file_name}")
                continue  # Skip to the next file if the layer is invalid

            print(f"Reprojecting: {file_name}")

            # Step 6: Define processing parameters for the reprojection
            processing_params = {
                'INPUT': layer,  # The layer to be reprojected
                'TARGET_CRS': 'EPSG:3857',  # Target CRS (Web Mercator)
                'OUTPUT': 'memory:'  # Store the reprojected layer temporarily in memory
            }

            feedback = QgsProcessingFeedback()  # Feedback object for monitoring the process

            try:
                # Step 7: Execute the "native:reprojectlayer" tool to reproject the layer
                result = processing.run("native:reprojectlayer", processing_params, feedback=feedback)
                reprojected_layer = result['OUTPUT']  # Get the reprojected layer result

                # Step 8: Check if the reprojected layer contains features (data)
                if reprojected_layer and reprojected_layer.featureCount() > 0:
                    output_path = os.path.join(output_folder, file_name)  # Define the path to save the reprojected layer
                    # Step 9: Save the reprojected layer to the output folder
                    QgsVectorFileWriter.writeAsVectorFormat(
                        reprojected_layer,
                        output_path,
                        "utf-8",  # Encoding format for the file
                        reprojected_layer.crs(),  # CRS of the reprojected layer
                        "GPKG"  # File format (GeoPackage)
                    )
                    print(f"Reprojected layer saved to: {output_path}")
                else:
                    print(f"No features found in {file_name}")

            except Exception as e:
                # Step 10: Handle any errors during processing
                print(f"Error processing {file_name}: {e}")

# Step 11: Define input and output folder paths (modify as necessary)
input_folder = r"C:\Users\Heron\Desktop\QGIS\NL BCA Building Segmentation\Boundaries\NL Municipal Boundaries\Municipal Boundaries Split Fix Geo"
output_folder = r"C:\Users\Heron\Desktop\QGIS\NL BCA Building Segmentation\Boundaries\NL Municipal Boundaries\Municipal Boundaries Split Fix Geo EPSG 3857"

# Step 12: Run the script to reproject layers
reproject_layers(input_folder, output_folder)
