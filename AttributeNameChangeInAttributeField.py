"""
Purpose: 
Update attribute values within a layer's attribute field of a QGIS project. It checks the values of a field in the layer and makes corrections based on certain conditions. 
In this case, the script corrects instances where the value of a field is incorrectly labeled as "garages" and updates it to "garage."

Inputs: 
Layer: The user can specify the layer within the QGIS project by its name (line 18 --> currently set as "Final_NL_Building_Layer_Copy — Final_Building_Layer").
QGIS MUST BE OPEN AND LAYER NAME MUST MATCH QGIS LAYER OPENED IN PROJECT
Field Name: The attribute field to be modified can be set (currently set as "building").
The value to be corrected ("garages") and the new value ("garage") can be customized for different corrections.

Date: 2025-02-07
Project: NL BCA Tool
"""

# Access the layer by name from the QGIS project
# Replace "Final_NL_Building_Layer_Copy — Final_Building_Layer" with the correct layer name in your project
layer = QgsProject.instance().mapLayersByName("Final_NL_Building_Layer_Copy — Final_Building_Layer")[0]  

# Specify the name of the field (attribute) to be updated
# Replace "building" with the appropriate field name in your dataset
field_name = "building"  

# Begin editing mode on the layer
layer.startEditing()

# Loop through all features (records) in the layer
for feature in layer.getFeatures():
    # Check if the value in the specified field matches "garages"
    if feature[field_name] == "garages":  # Look for the incorrect value
        feature[field_name] = "garage"    # Correct the value to "garage"
        # Update the feature in the layer with the new value
        layer.updateFeature(feature)      

# Commit the changes (save them)
layer.commitChanges()

# Print a message to confirm that the changes were made successfully
print("Attribute values updated successfully!")

