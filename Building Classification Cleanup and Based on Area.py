"""
# Purpose:
# PyQGIS script applies a 'CASE' field calculation to categorize building types based on the "building" and "building_area" fields.
# The user can import a shapefile from their directory or select an existing file from the QGIS project.

# Inputs:
# - A shapefile or vector layer containing the "building" and "building_area" fields.
# - The user can choose the file via QGIS GUI or provide a file path manually.

# Date: February 7, 2025
# Project: NL BCA Tool
"""

from qgis.core import (
    QgsProject, QgsVectorLayer, QgsField, QgsExpression, QgsExpressionContext, QgsExpressionContextUtils
)
from PyQt5.QtCore import QVariant
from qgis.utils import iface

# Function to apply the field calculation
def apply_case_expression(layer):
    # Add a new field to store the result of the CASE expression
    field_name = 'building_category'
    if field_name not in [field.name() for field in layer.fields()]:
        layer.startEditing()
        layer.dataProvider().addAttributes([QgsField(field_name, QVariant.String)])
        layer.updateFields()
        layer.commitChanges()

    # Create the CASE expression for the 'building' and 'building_area' fields
    case_expression = """
    CASE
        WHEN "building" IN ('greenhouse', 'stable', 'farm_auxiliary', 'farm', 'barn') THEN 'Agricultural'
        WHEN "building" IN ('retail', 'commercial', 'office', 'service', 'supermarket', 'post_office', 'hotel', 'restaurant') THEN 'Commercial'
        WHEN "building" IN ('fire_station') THEN 'Fire Station'
        WHEN "building" IN ('hospital', 'medical') THEN 'Hospital'
        WHEN "building" IN ('industrial', 'manufacture', 'warehouse') THEN 'Industrial'
        WHEN "building" IN ('school', 'college', 'government', 'university', 'kindergarten', 'Nova Central School District', 'school;yes') THEN 'Institutional & Government'
        WHEN "building" IN ('public', 'civic', 'stadium', 'toilets', 'parliament', 'sports_hall') THEN 'Public & Civic Infrastructure'
        WHEN "building" IN ('terrace', 'bar', 'sports_centre', 'brewery', 'gazebo') THEN 'Recreation & Leisure'
        WHEN "building" IN ('church', 'cathedral') THEN 'Religious Institution'
        WHEN "building" IN ('house') THEN 'Residential (house)'
        WHEN "building" IN ('cabin') THEN 'Residential (cabin)'
        WHEN "building" IN ('residential') THEN 'Residential (general)'
        WHEN "building" IN ('apartments') THEN 'Residential (appartments)'
        WHEN "building" IN ('detached') THEN 'Residential (detached)'
        WHEN "building" IN ('semidetached_house') THEN 'Residential (semidetached)'
        WHEN "building" IN ('dormitory') THEN 'Residential (dormitory)'
        WHEN "building" IN ('static_caravan') THEN 'Residential (static_caravan)'
        WHEN "building" IN ('Fishing_Stage', 'tent', 'hut', 'boathouse') THEN 'Temporary & Informal Structures'
        WHEN "building" IN ('transportation', 'hangar', 'parking', 'train_station', 'storage_tank') THEN 'Transportation & Utilities'
        WHEN "building" IN ('aircraft', 'ruins', 'construction', 'porch', 'carport') THEN 'Under Construction / Miscellaneous'
        WHEN "building" IN ('shed', 'garage', 'storage') THEN 'Storage'
        WHEN "building" IS NULL OR "building" = 'roof' THEN
            CASE
                WHEN "building_area" <= 50 THEN 'Storage'
                WHEN "building_area" > 50 AND "building_area" <= 200 THEN 'Residential (general)'
                WHEN "building_area" > 200 AND "building_area" <= 1200 THEN 'Commercial'
                WHEN "building_area" > 1200 THEN 'Industrial'
            END
    END
    """

    # Prepare the expression context
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

    # Apply the CASE expression for each feature in the layer
    expression = QgsExpression(case_expression)
    if expression.isValid():
        layer.startEditing()
        for feature in layer.getFeatures():
            context.setFeature(feature)
            result = expression.evaluate(context)
            # Update the field with the result
            feature.setAttribute(feature.fieldNameIndex(field_name), result)
            layer.updateFeature(feature)
        layer.commitChanges()
        print("Building categories updated successfully.")
    else:
        print("Invalid expression!")

# Prompt the user to select a file (QGIS interface) or specify a file path manually
def select_layer():
    # Check if there's an active layer in the project
    layer = iface.activeLayer()

    # If no active layer is selected, ask the user to load a file
    if not layer:
        file_path = iface.getOpenFileName(None, "Select a Shapefile", "", "Shapefiles (*.shp)")[0]
        if file_path:
            layer = QgsVectorLayer(file_path, "Imported Layer", "ogr")
            if not layer.isValid():
                print("Failed to load the layer.")
                return
            QgsProject.instance().addMapLayer(layer)
        else:
            print("No file selected.")
            return
    
    apply_case_expression(layer)

# Run the function to either select a layer or use the active layer in QGIS
select_layer()
