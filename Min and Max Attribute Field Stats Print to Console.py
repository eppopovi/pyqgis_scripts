"""
Purpose: 
This script processes a layer in QGIS to compute the minimum and maximum values for each building class. 
It calculates the minimum and maximum values for two attributes: 
1. Building Area
2. Compactness Index (CI)

Inputs:
1. User can modify the layer name in the script. The script is set to load a layer named "Final_NL_Building_Layer_With_Areas_Cleaned". 
   - This is where you specify the layer from your QGIS project to be processed (line 26).
2. The attributes in the script (e.g., "Building_Class", "Building_Area", and "Compactness_Index") 
should be updated if the attribute names in the layer differ (lines 38 to 40).

Outputs:
1. The script prints out the minimum and maximum values for each building class, showing the range for the building area and compactness index.
   - Output format: "{Building Class}: Area Min = X, Area Max = Y, CI Min = Z, CI Max = W"

Date: February 7, 2025
Project: NL BCA Tool
"""

from collections import defaultdict
from qgis.core import QgsProject

# Load the active layer by its name from the current QGIS project
# The layer "Final_NL_Building_Layer_With_Areas_Cleaned" should already exist in your project.
layer = QgsProject.instance().mapLayersByName("Final_NL_Building_Layer_With_Areas_Cleaned")[0]

# Create a defaultdict to store statistics (min/max) for each building class
# The defaultdict ensures that any new building class has default values: 
# inf (infinity) for min values and -inf (negative infinity) for max values initially.
stats = defaultdict(lambda: {"area_min": float("inf"), "area_max": float("-inf"),
                             "ci_min": float("inf"), "ci_max": float("-inf")})

# Loop through each feature (building) in the layer to gather and compare attribute values
for feature in layer.getFeatures():
    # Extract the necessary values from each feature
    building_class = feature["Building_Class"]  # The building's class
    area = feature["Building_Area"]  # The building's area
    compactness = feature["Compactness_Index"]  # The building's compactness index
    
    # Check if the values for building_class, area, and compactness are valid (non-null)
    if building_class and area is not None and compactness is not None:
        # For the current building class, update the minimum and maximum values for area and compactness
        stats[building_class]["area_min"] = min(stats[building_class]["area_min"], area)
        stats[building_class]["area_max"] = max(stats[building_class]["area_max"], area)
        stats[building_class]["ci_min"] = min(stats[building_class]["ci_min"], compactness)
        stats[building_class]["ci_max"] = max(stats[building_class]["ci_max"], compactness)

# After processing all features, print the results
# This will show the minimum and maximum values for area and compactness for each building class
for building_class, values in stats.items():
    print(f"{building_class}: Area Min = {values['area_min']}, Area Max = {values['area_max']}, \
          CI Min = {values['ci_min']}, CI Max = {values['ci_max']}")
