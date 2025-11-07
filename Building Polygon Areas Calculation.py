"""
Purpose:
This script calculates the area of polygons in an active vector layer in QGIS and stores the result in a new field called 'building_area'. 
The area is calculated in square meters and rounded to one decimal place. It ensures that the vector layer is valid and handles CRS transformations to ensure accurate area calculation. 

Inputs:
- The active layer must be a valid vector layer containing polygon features. 
- The layer should have a defined coordinate reference system (CRS) for proper transformation.
- Modify the target CRS (line 44) if necessary, based on the specific region or CRS required.
- The field name for the area calculation can be changed by modifying `area_field` (line 31).

Date: February 7, 2025
Project: NL BCA Tool
"""

from qgis.core import (
    QgsProject, QgsVectorLayer, QgsField, QgsFeature, QgsUnitTypes, QgsCoordinateReferenceSystem,
    QgsCoordinateTransform, QgsDistanceArea
)
from PyQt5.QtCore import QVariant

# Step 1: Load the active vector layer from QGIS
layer = iface.activeLayer()

# Step 2: Check if the layer is valid
if not layer or not layer.isValid():
    print("No valid vector layer selected!")  # If the layer is not valid, print an error and exit the script.
    exit()

# Step 3: Define the field name where the area will be stored
area_field = "building_area"

# Step 4: Check if the field already exists in the attribute table
fields = [field.name() for field in layer.fields()]  # Get a list of field names in the layer.
layer.startEditing()  # Start editing the layer to allow modifications.

# Step 5: If the area field doesn't exist, add it to the layer
if area_field not in fields:
    # Add the 'building_area' field with data type 'Double' and a precision of 1 decimal place.
    layer.dataProvider().addAttributes([QgsField(area_field, QVariant.Double, "double", 10, 1)])  
    layer.updateFields()  # Update the layer fields to reflect the new attribute.

# Step 6: Define the target CRS (Coordinate Reference System) for Newfoundland & Labrador (EPSG:3857)
target_crs = QgsCoordinateReferenceSystem("EPSG:3857")  # UTM Zone 21N is an example; change to your local CRS if needed.

# Step 7: Set up the coordinate transformation from the layer's CRS to the target CRS
transform = QgsCoordinateTransform(layer.crs(), target_crs, QgsProject.instance())

# Step 8: Set up the distance calculator to compute area in the target CRS
distance_calculator = QgsDistanceArea()
distance_calculator.setSourceCrs(target_crs, QgsProject.instance().transformContext())

# Step 9: Loop through all features in the layer and calculate their areas
for feature in layer.getFeatures():
    geom = feature.geometry()  # Get the geometry of the feature (polygon).
    
    if geom and geom.isGeosValid():  # Ensure the geometry is valid.
        # Step 10: Reproject geometry to the target CRS
        transformed_geom = geom.transform(transform)
        
        # Step 11: Calculate the area of the polygon in square meters
        area = distance_calculator.measureArea(geom)
        
        # Step 12: Round the area to 1 decimal place
        rounded_area = round(area, 1)
        
        # Step 13: Update the feature's attribute with the calculated area
        feature.setAttribute(layer.fields().indexFromName(area_field), rounded_area)  
        layer.updateFeature(feature)  # Save the updated feature in the layer.

# Step 14: Commit changes to the layer to save the updated attributes
layer.commitChanges()

# Step 15: Print confirmation message
print("Polygon areas correctly calculated and stored in 'building_area' field with 1 decimal place precision!")
