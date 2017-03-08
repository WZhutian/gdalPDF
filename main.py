
# -*- coding:utf-8 -*-
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from ogr2vrt import *
from md import *
gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","YES")
gdal.SetConfigOption("SHAPE_ENCODING","")
inputFilePath = "F:/GDALpdf/data/"
outputFilePath = "F:/GDALpdf/data/"
#1.生成vrt文件 使用开源代码
outputVRT = "temp.vrt"
inputFileName = "road_1.shp"
print ogr2vrt(inputFilePath+inputFileName,outputVRT)
# os.system("python ogr2vrt.py " + outputVRT + " " + inputFileName)

exit()
#使用python替换命令行
# option = gdal.RasterizeOptions(xRes="0.0001", yRes="0.0001", burnValues="0" , outputBounds="Byte" )
# print gdal.Rasterize(destNameOrDestDS="F:/GDALpdf/data/node_2.tif",srcDS='F:/GDALpdf/data/node_extent.shp', burnValues=0)
#原句
outputExtent = filePath + "node_extent.shp"
outputRaster = filePath + "node.tif"
os.system("gdal_rasterize -burn 255  "  + outputExtent + " " + outputRaster)


path="F:/GDALpdf/data/road_1.tif"
driver = gdal.GetDriverByName( "PDF" )
ds = gdal.Open(path)
dst_filename = "11111.pdf"
# dst_ds = driver.CreateCopy( dst_filename, ds, 0 ,[ 'OGR_DATASOURCE=road_1.vrt',"OGR_DISPLAY_FIELD=FID"])
