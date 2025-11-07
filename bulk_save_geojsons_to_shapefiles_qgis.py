import os
from qgis.core import (
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext
)

# --- USER INPUT ---
input_dir = r"C:\Path\To\Geojsons"
output_dir = r"C:\Path\To\Shapefiles"
# -------------------

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.lower().endswith(".geojson"):
        geojson_path = os.path.join(input_dir, filename)
        shp_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".shp")

        # Load the GeoJSON
        layer = QgsVectorLayer(geojson_path, filename, "ogr")
        if not layer.isValid():
            print(f"❌ Failed to load {filename}")
            continue

        # Create save options
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "ESRI Shapefile"
        options.fileEncoding = "UTF-8"

        # Save to Shapefile
        error = QgsVectorFileWriter.writeAsVectorFormatV3(
            layer,
            shp_path,
            QgsCoordinateTransformContext(),
            options
        )

        if error[0] == QgsVectorFileWriter.NoError:
            print(f"✅ Converted {filename} → {os.path.basename(shp_path)}")
        else:
            print(f"⚠️ Error converting {filename}: {error}")
