gdal_translate
-of PDF
-a_srs epsg:3857
test.tif
test.pdf
-projwin_srs epsg:3857
-co LAYER_NAME="test"
-co OGR_DATASOURCE=test.vrt
-co OGR_DISPLAY_FIELD="connectIDs"
-co OGR_DISPLAY_LAYER_NAMES="road_1"
-co EXTRA_IMAGES=Lena.jpg,200,0,0.1
-co EXTRA_LAYER_NAME="cow"


1.
python ogr2vrt.py road_1.shp road_1.vrt
python ogr2vrt.py node.shp node.vrt


2.
ogrtindex -accept_different_schemas road_1_extent.shp road_1.shp

gdal_rasterize -burn 0 -ot Byte -tr 0.0001 0.0001 node_extent.shp node.tif


3.
 gdal_translate -of PDF
 -a_srs EPSG:4326
 -co OGR_DATASOURCE=temp.vrt
 -co OGR_DISPLAY_FIELD="FID"
 temp.tif
 node.pdf
