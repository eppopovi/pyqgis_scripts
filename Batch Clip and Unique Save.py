"""
# Purpose: 
# This script automates the process of clipping building layer features with multiple zone layers. 
# It takes a building layer and clips it against specified zone layers, saving the resulting clipped layers to a designated output folder.
# 
# Inputs:
# 1. **input_building_layer_path** - Specify the path to the input building layer where the features to be clipped are stored (line 29).
# 2. **overlay_layers_paths** - Specify the paths to the overlay zone layers used for clipping (line 30). You can modify the number of layers by adjusting the range of the `overlay_layers_paths` list (line 17).
# 3. **output_folder** - Specify the directory where the resulting clipped layers will be saved (line 37).
#
# Date: February 07, 2025
# Project: NL BCA Tool
"""

from qgis.core import (
    QgsVectorLayer,
    QgsProcessingFeedback,
    QgsProcessingAlgorithm,
    QgsProject,
    QgsVectorFileWriter
)
from qgis.analysis import QgsNativeAlgorithms

# Ensure the QGIS processing algorithms are available
import processing
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# Input layers
input_building_layer_path = r"C:\Users\Heron\Desktop\Clipped\Segmentation\Merged Bounding Boxes\merged_bounding_boxes.gpkg"  # Replace with the path to your building layer
overlay_layers_paths = [
    fr"C:\Users\Heron\Desktop\QGIS\NL BCA Building Segmentation\Case Studies\Case Study Boundaries\fid_{i}.gpkg"
    for i in range(8, 10)
]
# Replace with your zones paths

# Output folder for the clipped layers
output_folder = r"C:\Users\Heron\Desktop\Clipped\Segmentation\Final Clipped to communities"  # Replace with the desired output folder

# Step 1: Load the input building layer
input_layer = QgsVectorLayer(input_building_layer_path, "Buildings", "ogr")
# Check if the input layer is valid (successfully loaded)
if not input_layer.isValid():
    print("Failed to load the input building layer.")
    exit()  # Exit if the layer is not loaded correctly

# Feedback for processing
feedback = QgsProcessingFeedback()

# Step 2: Loop through each overlay layer and perform the clip operation
for idx, overlay_path in enumerate(overlay_layers_paths, start=1):
    # Step 3: Load the overlay zone layer
    overlay_layer = QgsVectorLayer(overlay_path, f"Zone_{idx}", "ogr")
    if not overlay_layer.isValid():
        # If the overlay layer fails to load, print an error and skip to the next zone
        print(f"Failed to load overlay layer: {overlay_path}")
        continue

    # Step 4: Define the output file path for the clipped layer
    output_path = f"{output_folder}{idx}.gpkg"

    # Step 5: Set parameters for the clip operation
    params = {
        "INPUT": input_layer,  # The building layer to be clipped
        "OVERLAY": overlay_layer,  # The zone layer to clip against
        "OUTPUT": output_path  # The output file path for the result
    }

    # Step 6: Perform the clip operation using QGIS's native clip algorithm
    result = processing.run("native:clip", params, feedback=feedback)
    
    # Step 7: Check if the clip operation was successful
    if result:
        print(f"Clipped layer saved: {output_path}")  # Notify user of success
    else:
        print(f"Clip operation failed for zone {idx}")  # Notify user if something went wrong

# Step 8: Notify that the batch processing has been completed for all zones
print("Batch processing completed.")
