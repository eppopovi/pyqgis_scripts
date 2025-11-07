"""
Purpose: 
This script calculates the average area of buildings grouped by their class. It retrieves data from the active layer in QGIS, 
which contains attribute fields for building area and class. For each building class, the script computes the total area 
and the count of buildings, then calculates and prints the average building area for each class. 
THIS CAN APPLY TO ANY AVERAGE CALCULATION BASED ON CLASS

Inputs:
- Line 2: Modify the attribute field name 'Building_Area' with the actual field name for the area data in your dataset.
- Line 3: Modify the attribute field name 'Building_Class' with the actual field name for the building class data in your dataset.
- The script works with the active layer from your GIS application (QGIS), so no external input is needed other than ensuring the layer is selected.

Date: February 7, 2025
Project: NL BCA Tool
"""

# Get the active layer
layer = iface.activeLayer()

# Name of the attribute field containing the area values
area_field = 'Building_Area'  # Replace with the actual name of your area field
building_class_field = 'Building_Class'  # Replace with the actual name of your building class field

# Create a dictionary to store total areas and counts for each building class
class_areas = {}

# Start iterating over features
for feature in layer.getFeatures():
    building_class = feature[building_class_field]  # Get the building class
    area = feature[area_field]  # Get the area from the attribute field

    # Initialize dictionary entries for each class if not already present
    if building_class not in class_areas:
        class_areas[building_class] = {'total_area': 0, 'count': 0}
    
    # Add the area to the total and increment the count for the class
    class_areas[building_class]['total_area'] += area
    class_areas[building_class]['count'] += 1

# Calculate and print the average area for each class
for building_class, data in class_areas.items():
    average_area = data['total_area'] / data['count'] if data['count'] > 0 else 0
    print(f"Average area for {building_class}: {average_area}")
