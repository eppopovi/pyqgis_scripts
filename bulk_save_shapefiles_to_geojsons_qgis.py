import os
from qgis.core import (
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext
)

# --- USER INPUT ---
input_dir = r"C:\Path\To\Shapefiles"
output_dir = r"C:\Path\To\Geojsons"
# -------------------

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.lower().endswith(".shp"):
        shp_path = os.path.join(input_dir, filename)
        geojson_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".geojson")

        # Load the shapefile
        layer = QgsVectorLayer(shp_path, filename, "ogr")
        if not layer.isValid():
            print(f"❌ Failed to load {filename}")
            continue

        # Create save options
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GeoJSON"
        options.fileEncoding = "UTF-8"

        # Save to GeoJSON
        error = QgsVectorFileWriter.writeAsVectorFormatV3(
            layer,
            geojson_path,
            QgsCoordinateTransformContext(),
            options
        )

        if error[0] == QgsVectorFileWriter.NoError:
            print(f"✅ Converted {filename} → {os.path.basename(geojson_path)}")
        else:
            print(f"⚠️ Error converting {filename}: {error}")
