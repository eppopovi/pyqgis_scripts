"""
Purpose:Process a layer from QGIS, extract the values from the Building_Class field, 
count the occurrences of each building class, and save the results to a CSV file. 
This can be useful for creating summaries of building classifications in a given dataset. 
If QGIS is not available, the script can also be modified to read a file from a specified directory, 
providing an alternative method for data input (option 2).

Inputs:
Layer Name: The layer in the QGIS project is specified by the mapLayersByName function (line 22) or by user directory in option 2 (line 39), which must match the name of the layer containing the building data.
Field Name: The field containing the building class names (i.e., Building_Class --> line 27) is defined in the script. You can change this field name depending on your dataset.
Output File: The script saves the results to a CSV file located at C:\Users\Heron\Desktop\output2.csv. You can modify the file path to specify a different output location.

Date: Feb 7, 2025

Project: NL BCA Tool
"""                                                                                                                                                                                                                                                                                                                                                                                                                           
# Import necessary libraries
from collections import Counter  # For counting occurrences of building class values
import csv  # For writing results to a CSV file

# Option 1: Process the data directly in QGIS (uncomment if QGIS is available)
# Set the layer name - this is where you specify the name of the layer in QGIS
layer = QgsProject.instance().mapLayersByName("Final_NL_Building_Layer_With_Areas_Cleaned_Copy")[0]  



# Define the attribute field containing the building classes (you can change this if the field name is different)
field_name = "Building_Class"

# Extract all values from the specified field for each feature in the layer
values = [feature[field_name] for feature in layer.getFeatures()]

# Count the occurrences of each unique building class using the Counter class
counts = Counter(values)

# Print the results in the console
for building_class, count in counts.items():
    print(f"{building_class}: {count}")

# Option 2: Uncomment the next section if QGIS is not available and you want to read from a file
# # Read the input data from a CSV file
# input_file = r"C:\path_to_your_directory\input_data.csv"
# with open(input_file, "r") as f:
#     reader = csv.DictReader(f)  # Use DictReader to handle CSV rows as dictionaries
#     values = [row[field_name] for row in reader]

# # Count the occurrences of each unique building class
# counts = Counter(values)

# # Print the results in the console
# for building_class, count in counts.items():
#     print(f"{building_class}: {count}")

# Specify the output file path to save the results
output_file = r"C:\Users\Heron\Desktop\output2.csv"

# Write the counts to the CSV file
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)  # Initialize CSV writer
    writer.writerow(["Building Class", "Count"])  # Write the header row
    for building_class, count in counts.items():
        writer.writerow([building_class, count])  # Write each building class and its count

# Confirm the results have been saved
print(f"Results saved to {output_file}")
