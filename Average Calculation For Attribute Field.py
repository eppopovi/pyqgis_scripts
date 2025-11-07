"""
Purpose: Script calculates and prints the average Compactness Index (CI) for each building class in a given GIS layer.
The average CI is calculated by summing the CI values of features grouped by their building class and dividing by the number of features in each class.

Inputs: 
The user should have an active GIS layer with at least two fields: one containing the Compactness Index (CI) values (specified in the `CI_field` variable) and the other containing the building class information (specified in the `building_class_field` variable).
The user can modify these fields to match the attribute names in their own GIS layer.

Date: 2025-02-07

Project: NL BCA Tool
"""

# Get the active layer from the GIS interface
layer = iface.activeLayer()  # `iface` is an object representing the QGIS interface, and `activeLayer()` retrieves the currently selected layer.

# Define the attribute field names for the Compactness Index (CI) and building class
CI_field = 'Compactness_Index'  # Replace with the actual name of your CI field in the layer's attributes
building_class_field = 'Building_Class'  # Replace with the actual name of your building class field

# Create a dictionary to store the total area and feature count for each building class
class_areas = {}  # This will hold the aggregated data for each building class (total area and feature count)

# Iterate through each feature (row) in the active layer
for feature in layer.getFeatures():  # `getFeatures()` returns all the features (objects) in the layer
    building_class = feature[building_class_field]  # Retrieve the building class for the current feature
    area = feature[CI_field]  # Retrieve the Compactness Index (CI) for the current feature

    # Check if the building class already exists in the dictionary; if not, initialize it
    if building_class not in class_areas:
        class_areas[building_class] = {'total_area': 0, 'count': 0}  # Initialize total area and count to 0

    # Update the total area and count for the current building class
    class_areas[building_class]['total_area'] += area  # Add the CI value to the total area for this building class
    class_areas[building_class]['count'] += 1  # Increment the feature count for this building class

# Now, calculate the average CI for each building class and print the results
for building_class, data in class_areas.items():  # Iterate over each building class and its data
    average_CI = data['total_area'] / data['count'] if data['count'] > 0 else 0  # Calculate the average CI for the class
    print(f"Average CI for {building_class}: {average_CI}")  # Output the average CI for the current building class

